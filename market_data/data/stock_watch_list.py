class StockWatchList:
    def __init__(self):
        self.watch_list = set()

    def add_stock(self, symbol):
        self.watch_list.add(symbol)

    def remove_stock(self, symbol):
        self.watch_list.discard(symbol)

    def get_watch_list(self):
        return list(self.watch_list)

def main():
    stock_watch_list = StockWatchList()
    stock_watch_list.add_stock('AAPL')
    stock_watch_list.add_stock('MSFT')
    print("Current Watch List:", stock_watch_list.get_watch_list())

if __name__ == "__main__":
    main()