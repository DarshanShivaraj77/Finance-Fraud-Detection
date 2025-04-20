import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def generate_transaction():
    return {
        "transaction_id": str(random.randint(100000, 999999)),
        "timestamp": datetime.now().isoformat(),
        "amount": round(random.uniform(10.0, 10000.0), 2),
        "source_account": f"ACC{random.randint(1000, 9999)}",
        "destination_account": f"ACC{random.randint(1000, 9999)}",
        "transaction_type": random.choice(["transfer", "withdrawal", "deposit"]),
    }

while True:
    transaction = generate_transaction()
    producer.send('raw-transactions', value=transaction)
    print(f"Produced: {transaction}")
    time.sleep(1)  # 1 second interval
