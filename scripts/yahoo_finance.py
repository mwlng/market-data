from market_data.yahoo import yfinance_async_websocket

async def run(tickers: list[str]):
    await yfinance_async_websocket.run(tickers)
