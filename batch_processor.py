import psycopg2
import pandas as pd

conn = psycopg2.connect(
    dbname="finance_fraud",
    user="frauddetection",
    password="password",
    host="localhost",
    port="5432"
)

query = """
SELECT
    date_trunc('minute', timestamp) as window_start,
    date_trunc('minute', timestamp) + interval '1 minute' as window_end,
    COUNT(*) as total_transactions,
    SUM(CASE WHEN is_flagged THEN 1 ELSE 0 END) as flagged_transactions,
    AVG(amount) as avg_transaction_amount,
    MAX(amount) as max_transaction_amount,
    'batch' as processing_mode,
    CURRENT_TIMESTAMP as processed_time
FROM transactions
GROUP BY window_start
ORDER BY window_start;
"""

df = pd.read_sql_query(query, conn)

# Optionally insert into analytics table
for _, row in df.iterrows():
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO analytics (window_start, window_end, total_transactions,
        flagged_transactions, avg_transaction_amount, max_transaction_amount,
        processing_mode, processed_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))
    conn.commit()

conn.close()
