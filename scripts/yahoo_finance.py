import json
from market_data.yahoo import yfinance_async_websocket
from market_data.yahoo.models.yfinance_data_model import create_stock_data_model

async def run(tickers: list[str], on_message: callable):
    await yfinance_async_websocket.run(tickers, on_message) 