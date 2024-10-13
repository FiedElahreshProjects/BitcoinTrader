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
    trade_profit_loss DECIMAL(10, 2),          -- P/L for the individual trade
    cumulative_profit_loss DECIMAL(10, 2),     -- Total P/L up to and including this trade
    decision_date DATE NOT NULL,
    capital DECIMAL(15, 2)                     -- Total capital remaining after this trade
);


INSERT INTO daily_sentiment (date, positive_score, neutral_score, negative_score, compound_score)
VALUES 
    (CURRENT_DATE - INTERVAL '13 days', 0.200, 0.700, 0.100, 0.250),
    (CURRENT_DATE - INTERVAL '12 days', 0.350, 0.600, 0.050, 0.400),
    (CURRENT_DATE - INTERVAL '11 days', 0.150, 0.500, 0.350, -0.200),
    (CURRENT_DATE - INTERVAL '10 days', 0.100, 0.600, 0.300, -0.150),
    (CURRENT_DATE - INTERVAL '9 days', 0.300, 0.600, 0.100, 0.320),
    (CURRENT_DATE - INTERVAL '8 days', 0.250, 0.650, 0.100, 0.280),
    (CURRENT_DATE - INTERVAL '7 days', 0.200, 0.600, 0.200, 0.000),
    (CURRENT_DATE - INTERVAL '6 days', 0.450, 0.500, 0.050, 0.500),
    (CURRENT_DATE - INTERVAL '5 days', 0.150, 0.700, 0.150, 0.050),
    (CURRENT_DATE - INTERVAL '4 days', 0.200, 0.650, 0.150, 0.150),
    (CURRENT_DATE - INTERVAL '3 days', 0.100, 0.500, 0.400, -0.300),
    (CURRENT_DATE - INTERVAL '2 days', 0.050, 0.500, 0.450, -0.350),
    (CURRENT_DATE - INTERVAL '1 day',  0.300, 0.600, 0.100, 0.200);


INSERT INTO daily_technical_analysis (date, closing_price, sma_7, sma_21, rsi)
VALUES 
    (CURRENT_DATE - INTERVAL '13 days', 40000.50, 39800.00, 39500.00, 45.30),
    (CURRENT_DATE - INTERVAL '12 days', 40500.20, 40000.50, 39700.00, 47.20),
    (CURRENT_DATE - INTERVAL '11 days', 39500.75, 39950.25, 39650.75, 42.10),
    (CURRENT_DATE - INTERVAL '10 days', 39000.30, 39800.80, 39500.50, 39.00),
    (CURRENT_DATE - INTERVAL '9 days', 40300.10, 40000.00, 39600.00, 49.00),
    (CURRENT_DATE - INTERVAL '8 days', 40700.60, 40200.50, 39700.50, 51.10),
    (CURRENT_DATE - INTERVAL '7 days', 41000.20, 40500.20, 39850.00, 53.50),
    (CURRENT_DATE - INTERVAL '6 days', 42000.50, 41000.00, 40000.00, 56.20),
    (CURRENT_DATE - INTERVAL '5 days', 41500.10, 41200.00, 40150.25, 54.50),
    (CURRENT_DATE - INTERVAL '4 days', 41800.75, 41350.30, 40200.50, 55.30),
    (CURRENT_DATE - INTERVAL '3 days', 42500.50, 41700.10, 40400.20, 60.20),
    (CURRENT_DATE - INTERVAL '2 days', 43000.25, 42000.00, 40650.75, 62.30),
    (CURRENT_DATE - INTERVAL '1 day',  42800.10, 42100.50, 40700.10, 61.50),
    (CURRENT_DATE, 42600.80, 42000.75, 40750.50, 59.00);

INSERT INTO weekly_trade_history 
(week_start_date, action, price, quantity, trade_profit_loss, cumulative_profit_loss, decision_date)
VALUES 
(CURRENT_DATE - INTERVAL '20 days', 'buy', 1020.00, 1.0000, 0.00, 0.00, CURRENT_DATE - INTERVAL '20 days'),
(CURRENT_DATE - INTERVAL '15 days', 'sell', 1090.00, 1.0000, 70.00, 70.00, CURRENT_DATE - INTERVAL '15 days'),
(CURRENT_DATE - INTERVAL '10 days', 'buy', 1055.00, 1.0000, 0.00, 70.00, CURRENT_DATE - INTERVAL '10 days'),
(CURRENT_DATE - INTERVAL '5 days', 'sell', 1085.00, 1.0000, 30.00, 100.00, CURRENT_DATE - INTERVAL '5 days');