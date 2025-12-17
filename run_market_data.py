#!/bin/env python

import asyncio
from postgres.db import PostgresDB
from scripts import yahoo_finance as yf

db_conn_string = 'postgresql://postgres:postgres@localhost:5432/market_data'
market_data_db = PostgresDB(db_conn_string)

def get_stock_watch_lists(list_size: int) -> list[list[str]]:
    query = "SELECT stock_symbol FROM watch_list;"
    results = market_data_db.execute_query(query)
    count = 0
    watch_list = []
    watch_lists = []
    for row in results:
        count += 1
        if count > list_size:
            watch_lists.append(watch_list)
            watch_list = []
            count = 1
        watch_list.append(row[0])

    if watch_list:    
        watch_lists.append(watch_list)
 
    return watch_lists


async def main():
    market_data_db.connect()
    stock_watch_lists =  get_stock_watch_lists(10)
    for l in stock_watch_lists:
        await yf.run(l)

    market_data_db.disconnect()

if __name__ == '__main__':
    asyncio.run(main())