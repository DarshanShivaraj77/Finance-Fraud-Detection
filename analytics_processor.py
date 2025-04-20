import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, current_timestamp, when, window, avg, max, count
from pyspark.sql.types import *

# Start Spark Session
spark = SparkSession.builder \
    .appName("Analytics Processor") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.postgresql:postgresql:42.2.5") \
    .getOrCreate()

# Define the schema for Kafka data
schema = StructType([
    StructField("transaction_id", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("amount", DoubleType()),
    StructField("source_account", StringType()),
    StructField("destination_account", StringType()),
    StructField("transaction_type", StringType()),
])

# Read from Kafka topic
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "raw-transactions") \
    .load()

# Parse the JSON and apply basic transformation
parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*") \
    .withColumn("processed_time", current_timestamp()) \
    .withColumn("is_flagged", when(col("amount") > 7500, True).otherwise(False)) \
    .withColumn("risk_score", col("amount") / 100.0)

# Apply 1-minute window aggregation
windowed_df = parsed_df \
    .withWatermark("timestamp", "1 minute") \
    .groupBy(
        window(col("timestamp"), "1 minute")
    ) \
    .agg(
        count("*").alias("total_transactions"),
        count(when(col("is_flagged") == True, True)).alias("flagged_transactions"),
        avg("amount").alias("avg_transaction_amount"),
        max("amount").alias("max_transaction_amount")
    ) \
    .withColumn("processed_time", current_timestamp()) \
    .selectExpr(
        "window.start as window_start", 
        "window.end as window_end", 
        "total_transactions", 
        "flagged_transactions", 
        "avg_transaction_amount", 
        "max_transaction_amount", 
        "'streaming' as processing_mode", 
        "processed_time"
    )

# Write to PostgreSQL
def write_analytics_to_postgres(batch_df, epoch_id):
    batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/finance_fraud") \
        .option("dbtable", "analytics") \
        .option("user", "frauddetection") \
        .option("password", "password") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

analytics_query = windowed_df.writeStream \
    .foreachBatch(write_analytics_to_postgres) \
    .outputMode("update") \
    .start()

analytics_query.awaitTermination()
