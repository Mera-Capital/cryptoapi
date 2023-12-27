import asyncio
from decimal import Decimal

from cryptoapi.api.interfaces import ExchangeInterface, HTTPClientInterface
from cryptoapi.api.entities import (
    Instrument, Section, Timeframe,
    Candle,
    Quotes,
    CurrencyIndexPrice,
    Position,
    Equity,
    OperationsSummary,
    CommandStatus,
    OrderType, OrderInfo,
)
from .client import DeribitClient
from .url import DeribitURL
from .mapping import _DERIBIT_MAPPER


class Deribit(DeribitClient, ExchangeInterface):
    def __init__(self, testnet: bool, client: HTTPClientInterface) -> None:
        super().__init__(client)
        self._url = DeribitURL(testnet)
        self._mapper = _DERIBIT_MAPPER

    async def get_instruments(self) -> list[Instrument]:
        async with asyncio.TaskGroup() as tg:
            btc = tg.create_task(self.get(self._url.instruments.format(currency="BTC")))
            eth = tg.create_task(self.get(self._url.instruments.format(currency="ETH")))
            usdc = tg.create_task(self.get(self._url.instruments.format(currency="USDC")))
            usdt = tg.create_task(self.get(self._url.instruments.format(currency="USDT")))
        result = [*btc.result(), *eth.result(), *usdc.result(), *usdt.result()]
        print(result)

        # for instrument_dict in sum(responses, []):
        #     try:
        #         instrument = self._mapper.load({'section': 'MAIN', 'model': instrument_dict}, market_dto.Instrument)
        #         instruments.append(instrument)
        #     except MappingError:
        #         continue
        # return instruments

    async def get_candles(
            self,
            instrument_title: str,
            section: Section,
            timeframe: Timeframe,
            date_from: int,
            date_to: int,
    ) -> list[Candle]:
        pass

    async def get_quotes(self, instrument_title: str, section: Section) -> Quotes:
        pass

    async def get_index_price(self, currency_pair: str, section: Section) -> CurrencyIndexPrice:
        pass

    async def get_equity(self, currency: str, section: Section, creds: dict[str, str]) -> Equity:
        pass

    async def get_position(self, instrument: Instrument, creds: dict[str, str]) -> Position:
        pass

    async def get_operations_summary(self, instrument: Instrument, creds: dict[str, str]) -> OperationsSummary:
        pass

    async def cancel_all_orders(self, instrument: Instrument, creds: dict[str, str]) -> CommandStatus:
        pass

    async def close_position(self, instrument: Instrument, creds: dict[str, str]) -> CommandStatus:
        pass

    async def buy(
            self,
            amount: Decimal,
            order_type: OrderType,
            instrument: Instrument,
            creds: dict[str, str],
    ) -> OrderInfo:
        pass

    async def sell(
            self,
            amount: Decimal,
            order_type: OrderType,
            instrument: Instrument,
            creds: dict[str, str],
    ) -> OrderInfo:
        pass

    async def check_credentials(self, creds: dict[str, str]) -> CommandStatus:
        pass
