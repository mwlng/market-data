create database if not exists market_data;

CREATE TABLE if not exists yfinance_data_stream (
    id STRING,
    price NUMERIC(10, 4),
    time NUMERIC(15, 0),
    exchange STRING,
    quote_type INTERGER,    
    market_hours INTERGER,
    change_percent NUMERIC(8, 7),
    day_volume STRING,
    change NUMERIC(8, 7),
    price_hint STRING
  );