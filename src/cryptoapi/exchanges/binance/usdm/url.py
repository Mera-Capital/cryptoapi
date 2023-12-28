class UsdmURL:
    def __init__(self, testnet: bool) -> None:
        self.prod_url = 'https://fapi.binance.com/'
        self.test_url = 'https://testnet.binancefuture.com/'
        self.base = self.test_url if testnet else self.prod_url

        # Public

        self.instruments = self.prod_url + 'fapi/v1/exchangeInfo'
