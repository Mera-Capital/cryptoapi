from decimal import Decimal

from cryptoapi.api.protocols import ExchangeProtocol, HTTPClientProtocol
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


class Deribit(DeribitClient, ExchangeProtocol):
    def __init__(self, testnet: bool, client: HTTPClientProtocol) -> None:
        super().__init__(client)
        self._url = DeribitURL(testnet)
        self._mapper = _DERIBIT_MAPPER

    async def get_instruments(self) -> list[Instrument]:
        pass

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
