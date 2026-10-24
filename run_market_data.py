#!/bin/env python

import asyncio
import pandas as pd
from postgres.db import PostgresDB
from scripts import yahoo_finance as yf
from rising_wave.rw import RisingWaveClient

db_conn_string = 'postgresql://postgres:postgres@localhost:5432/market_data'
market_data_db = PostgresDB(db_conn_string)
rw = RisingWaveClient(database='market_data')
rw.create_schema('yfinance')

def get_stock_watch_lists(watch_groups: int)-> list[list[str]]:
    watch_lists = []

    query = "SELECT COUNT(*) FROM watch_list;"
    results = market_data_db.execute_query(query) 
    total_stocks = results[0][0]
    list_size = total_stocks // watch_groups + (1 if total_stocks % watch_groups > 0 else 0)
    if list_size == 0:
        return watch_lists
    else:          
        query = "SELECT stock_symbol FROM watch_list;"
        results = market_data_db.execute_query(query)
        count = 0
        watch_list = []
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


async def on_message(message):
    df=pd.DataFrame([message])
    rw.insert_dataframe(table='stock_data_stream', df=df)
    #json_data = json.dumps(message)
    #print(json_data)


task_groups = 2
async def main():
    try:
        market_data_db.connect()
        stock_watch_lists =  get_stock_watch_lists(task_groups)
        try:
            tasks = []
            async with asyncio.TaskGroup() as tg:
                # Tasks are scheduled immediately upon creation within the 'async with' block
                for watch_list in stock_watch_lists:
                    tasks.append(tg.create_task(yf.run(watch_list, on_message)))
        except ExceptionGroup as eg:
            # Handle exceptions if any task failed
            print(f"Caught exception group: {eg.exceptions}")
    finally:
        market_data_db.disconnect()


if __name__ == '__main__':
    asyncio.run(main())