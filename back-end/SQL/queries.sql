CREATE TABLE daily_sentiment (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    positive_score DECIMAL(4, 3) DEFAULT 0,
    neutral_score DECIMAL(4, 3) DEFAULT 0,
    negative_score DECIMAL(4, 3) DEFAULT 0,
    compound_score DECIMAL(4, 3) NOT NULL
);

CREATE TABLE daily_technical_analysis (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    closing_price DECIMAL(10, 2) NOT NULL,
    sma_7 DECIMAL(10, 2),        -- 7-day simple moving average
    sma_21 DECIMAL(10, 2),       -- 21-day simple moving average
    rsi DECIMAL(5, 2)            -- 14-day Relative Strength Index
);

CREATE TABLE weekly_trade_history (
    trade_id SERIAL PRIMARY KEY,
    week_start_date DATE NOT NULL,
    action VARCHAR(10) NOT NULL CHECK (action IN ('buy', 'sell', 'hold')),
    price DECIMAL(10, 2) NOT NULL,
    quantity DECIMAL(10, 4) NOT NULL,
    profit_loss DECIMAL(10, 2),
    decision_date DATE NOT NULL,
);