class WSSBinanceUMURL:
    def __init__(self, testnet: bool) -> None:
        self.prod_url = "wss://fstream.binance.com/ws"
        self.test_url = "wss://stream.binancefuture.com/ws"

        self.base = self.test_url if testnet else self.prod_url
