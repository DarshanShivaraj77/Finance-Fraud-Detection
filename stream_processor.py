import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, current_timestamp, when
from pyspark.sql.types import *

spark = SparkSession.builder \
    .appName("Finance Fraud Detection") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.postgresql:postgresql:42.2.5") \
    .getOrCreate()

schema = StructType([
    StructField("transaction_id", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("amount", DoubleType()),
    StructField("source_account", StringType()),
    StructField("destination_account", StringType()),
    StructField("transaction_type", StringType()),
])

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "raw-transactions") \
    .load()

# Parse the JSON
parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*") \
    .withColumn("processed_time", current_timestamp()) \
    .withColumn("is_flagged", when(col("amount") > 7500, True).otherwise(False)) \
    .withColumn("risk_score", col("amount") / 100.0)

# Write to PostgreSQL
def write_to_postgres(batch_df, epoch_id):
    batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/finance_fraud") \
        .option("dbtable", "transactions") \
        .option("user", "frauddetection") \
        .option("password", "password") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

query = parsed_df.writeStream \
    .foreachBatch(write_to_postgres) \
    .outputMode("update") \
    .start()

query.awaitTermination()
