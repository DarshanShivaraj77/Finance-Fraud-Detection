Finance Fraud Detection System

Real-time and Batch Fraud Detection using Spark, Kafka, and PostgreSQL

Tech Stack
Apache Spark
Kafka
PostgreSQL

📌 Overview
This project implements a real-time fraud detection system using:

Apache Spark (Streaming + Batch processing)

Apache Kafka (Message queue for transactions)

PostgreSQL (Database for storing transactions & fraud analytics)

The system flags suspicious transactions based on:
✔ Unusual transaction amounts
✔ High-frequency transactions
✔ Geographical anomalies
✔ New device logins

⚙️ Installation & Setup
1. Prerequisites
Ubuntu 22.04+ (Recommended)

Python 3.10+

Java JDK 21

PostgreSQL 15

2. Install Dependencies
Run the following commands:

bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Java (Spark dependency)
sudo apt install openjdk-21-jdk -y
java -version  # Verify installation

# Install Python & pip
sudo apt install python3 python3-pip -y
python3 --version

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y
sudo systemctl start postgresql
sudo systemctl enable postgresql
3. Install Required Python Packages
bash
pip install pyspark kafka-python psycopg2-binary pandas matplotlib findspark
4. Install Apache Spark
bash
# Download Spark
wget https://dlcdn.apache.org/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz
tar -xvzf spark-3.5.1-bin-hadoop3.tgz
sudo mv spark-3.5.1-bin-hadoop3 /opt/spark

# Add Spark to PATH
echo 'export SPARK_HOME=/opt/spark' >> ~/.bashrc
echo 'export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin' >> ~/.bashrc
source ~/.bashrc
5. Install Apache Kafka
bash
# Download Kafka
wget https://downloads.apache.org/kafka/3.6.0/kafka_2.13-3.6.0.tgz
tar -xvzf kafka_2.13-3.6.0.tgz
sudo mv kafka_2.13-3.6.0 /opt/kafka

# Start Zookeeper & Kafka
/opt/kafka/bin/zookeeper-server-start.sh -daemon /opt/kafka/config/zookeeper.properties
/opt/kafka/bin/kafka-server-start.sh -daemon /opt/kafka/config/server.properties
🚀 Running the Project
1. Start PostgreSQL & Create Tables
bash
sudo -u postgres psql
Run the SQL script:

sql
CREATE DATABASE fraud_detection;

\c fraud_detection;

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50),
    amount FLOAT,
    timestamp TIMESTAMP,
    merchant VARCHAR(100),
    location VARCHAR(100),
    is_fraud BOOLEAN
);

CREATE TABLE analytics (
    window_start TIMESTAMP,
    processing_mode VARCHAR(20),
    total_transactions INT,
    fraud_count INT,
    avg_transaction_amount FLOAT
);
2. Run Transaction Producer (Simulates Transactions)
bash
python3 transaction_producer.py
3. Start Spark Streaming Fraud Detection
bash
python3 stream_processor.py
4. Run Batch Processing (Optional)
bash
python3 batch_processor.py
📂 Project Structure
finance-fraud-detection/
├── transaction_producer.py   # Simulates transactions → Kafka
├── stream_processor.py       # Real-time fraud detection (Spark Streaming)
├── batch_processor.py        # Batch fraud analytics (Spark SQL)
├── config/
│   ├── kafka_config.py       # Kafka broker settings
│   └── db_config.py          # PostgreSQL credentials
├── screenshots/              # Output & terminal logs
└── README.md
📊 Results & Screenshots
Streaming Mode	Batch Mode
Streaming Output	Batch Output
📜 License
This project is licensed under MIT License.

🙌 Contributors

Bharath Gowda M

Darshan Shivaraj

Chetan Naik
