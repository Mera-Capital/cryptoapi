class SpotURL:
    def __init__(self) -> None:
        self.prod_url = 'https://api.binance.com/'
        # Public

        self.instruments = self.prod_url + 'api/v3/exchangeInfo'
