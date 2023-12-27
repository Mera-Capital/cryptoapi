class DeribitURL:
    def __init__(self, testnet: bool) -> None:
        self.prod_url = "https://www.deribit.com/api/v2/"
        self.test_url = "https://test.deribit.com/api/v2/"
        self.base = self.test_url if testnet else self.prod_url

        # Public
        self.auth = self.base + ("public/auth?client_id={client_id}&"
                                 "client_secret={client_secret}&"
                                 "grant_type=client_credentials")
        self.quotes = self.base + "public/ticker?instrument_name={instrument_name}"
        self.candles = self.base + ("public/get_tradingview_chart_data?instrument_name={instrument_name}&"
                                    "resolution={resolution}&"
                                    "start_timestamp={start_timestamp}&"
                                    "end_timestamp={end_timestamp}")
        self.index_price = self.base + "public/get_index_price?index_name={index_name}"
        self.instruments = self.base + "public/get_instruments?currency={currency}&kind=future"

        # Private
        self.equity = self.base + "private/get_account_summary?extended=true&currency={currency}"
        self.withdrawals = self.base + "private/get_withdrawals?count=100000&currency={currency}"
        self.deposits = self.base + "private/get_deposits?count=100000&currency={currency}"
        self.transfers = self.base + "private/get_transfers?count=100000&currency={currency}"
        self.position = self.base + "private/get_position?instrument_name={instrument_name}"
        self.buy = self.base + "private/buy?type={order_type}&amount={amount}&instrument_name={instrument_name}"
        self.sell = self.base + "private/sell?type={order_type}&amount={amount}&instrument_name={instrument_name}"
        self.cancel_orders = self.base + ("private/cancel_all_by_instrument?instrument_name={instrument_name}&"
                                          "type=all&"
                                          "detailed=false&"
                                          "include_combos=true")
        self.close_position = self.base + "private/close_position?instrument_name={instrument_name}&type=market"
