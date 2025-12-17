#!/bin/env python

import asyncio
import yfinance as yf
from models.yfinance_data_model import *

yfinance_wss = 'wss://streamer.finance.yahoo.com/?version=2'

async def on_message(message):
    stock_data = create_stock_data_model(message)
    print(stock_data)


async def run(tickers: list[str]):
    wss = yf.AsyncWebSocket(yfinance_wss)
    await wss.subscribe(tickers)
    try:
        await wss.listen(on_message)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    asyncio.run(run())

