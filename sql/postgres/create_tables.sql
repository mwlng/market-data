-- Create market data tables;
-- 
-- - stocks table
-- - watch_list table
--

create table if not exists stocks (
    id serial primary key,
    symbol varchar(10) not null unique,
    exchange varchar(30),
    currency varchar(10),
    industry varchar(100),
    sector varchar(100),
    short_name varchar(100),
    description text,
    updated_at timestamp default current_timestamp
);

create table if not exists watch_list (
    id serial primary key,
    stock_symbol varchar(10) references stocks(symbol) on delete cascade,
    created_at timestamp default current_timestamp,
    unique(stock_symbol)
); 

create table if not exists trading_book (
    id serial primary key,
    stock_symbol varchar(10) references stocks(symbol) on delete cascade,
    quantity integer not null,
    price numeric(12, 4) not null,
    trade_type varchar(10) not null, -- BUY or SELL
    trade_date date not null,   
    updated_at timestamp default current_timestamp
);