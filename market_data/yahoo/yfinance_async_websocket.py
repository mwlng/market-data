#!/bin/env python
import yfinance as yf

yfinance_wss = 'wss://streamer.finance.yahoo.com/?version=2'

async def run(tickers: list[str], on_message_func):
    wss = yf.AsyncWebSocket(yfinance_wss)
    await wss.subscribe(tickers)
    try:
        await wss.listen(on_message_func)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await wss.close()    
