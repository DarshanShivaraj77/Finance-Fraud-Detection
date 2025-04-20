# Finance Fraud Detection System  
**Real-time and Batch Fraud Detection using Spark, Kafka, and PostgreSQL**  

![Tech Stack](https://img.shields.io/badge/Apache_Spark-v3.5.1-orange) ![Kafka](https://img.shields.io/badge/Apache_Kafka-v3.6.0-blue) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-v15-green)  

---

## 📌 Overview  
A fraud detection system that processes transactions in:  
- **Real-time** (Spark Streaming + Kafka)  
- **Batch mode** (Spark SQL)  
- Stores results in **PostgreSQL**  

Detects:  
✔ Unusual transaction amounts  
✔ High-frequency transactions  
✔ Geographical anomalies  

---

## ⚙️ Installation  

### 1. Prerequisites  
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install openjdk-21-jdk python3 python3-pip postgresql postgresql-contrib -y
2. Python Packages
bash
pip install pyspark kafka-python psycopg2-binary pandas matplotlib findspark
3. Install Spark
bash
wget https://dlcdn.apache.org/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz
tar -xvzf spark-3.5.1-bin-hadoop3.tgz
sudo mv spark-3.5.1-bin-hadoop3 /opt/spark
echo 'export SPARK_HOME=/opt/spark' >> ~/.bashrc
echo 'export PATH=$PATH:$SPARK_HOME/bin' >> ~/.bashrc
source ~/.bashrc
4. Install Kafka
bash
wget https://downloads.apache.org/kafka/3.6.0/kafka_2.13-3.6.0.tgz
tar -xvzf kafka_2.13-3.6.0.tgz
sudo mv kafka_2.13-3.6.0 /opt/kafka
🚀 Running the System
1. Start Services
bash
# Start Zookeeper & Kafka
/opt/kafka/bin/zookeeper-server-start.sh -daemon /opt/kafka/config/zookeeper.properties
/opt/kafka/bin/kafka-server-start.sh -daemon /opt/kafka/config/server.properties

# Start PostgreSQL
sudo systemctl start postgresql
2. Setup Database
bash
sudo -u postgres psql -c "CREATE DATABASE fraud_detection;"
sudo -u postgres psql -d fraud_detection -c "
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50),
    amount FLOAT,
    timestamp TIMESTAMP,
    is_fraud BOOLEAN
);"
3. Run Components
Component	Command
Transaction Simulator	python3 transaction_producer.py
Streaming Detection	python3 stream_processor.py
Batch Processing	python3 batch_processor.py
📂 Project Structure
.
├── transaction_producer.py   # Kafka producer
├── stream_processor.py       # Real-time detection
├── batch_processor.py        # Batch analysis
├── config/
│   ├── kafka_config.py       # Broker settings
│   └── db_config.py          # DB credentials
└── README.md
📜 License
MIT License

🙌 Contributors
Bharath Gowda M

Darshan Shivaraj

Chetan Naik


**Key features of this README:**  
1. **Copy-Paste Friendly**: All commands are in ready-to-use code blocks  
2. **Minimal Dependencies**: Only essential installation steps  
3. **Structured Flow**: Follows standard GitHub project documentation format  
4. **Responsive Badges**: Shows tech stack at a glance  

You can paste this directly into a new `README.md` file in your project root. Let me know if yo
