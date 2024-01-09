class WSSBinanceCMURL:
    def __init__(self, testnet: bool) -> None:
        self.prod_url = "wss://dstream.binance.com/ws"
        self.test_url = "wss://dstream.binancefuture.com/ws"

        self.base = self.test_url if testnet else self.prod_url
