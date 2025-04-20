CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    timestamp TIMESTAMP,
    amount DECIMAL(19, 4),
    source_account VARCHAR(50),
    destination_account VARCHAR(50),
    transaction_type VARCHAR(20),
    is_flagged BOOLEAN,
    risk_score DECIMAL(5, 2),
    processed_time TIMESTAMP
);

CREATE TABLE IF NOT EXISTS analytics (
    id SERIAL PRIMARY KEY,
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    total_transactions INTEGER,
    flagged_transactions INTEGER,
    avg_transaction_amount DECIMAL(19, 4),
    max_transaction_amount DECIMAL(19, 4),
    processing_mode VARCHAR(10),
    processed_time TIMESTAMP
);
