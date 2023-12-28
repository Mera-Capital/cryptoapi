import asyncio
from decimal import Decimal

from cryptoapi import ExchangeInterface
from cryptoapi.api.entities import (
    Instrument,
    Section,
    Timeframe,
    Candle,
    Quotes,
    CurrencyIndexPrice,
    Equity,
    Position,
    OperationsSummary,
    CommandStatus,
    OrderType,
    OrderInfo
)
from cryptoapi.api.interfaces import HTTPClientInterface
from .usdm import BinanceUsdm
from .coinm import BinanceCoinm
from .spot import BinanceSpot


class Binance(ExchangeInterface):
    def __init__(self, testnet: bool, client: HTTPClientInterface) -> None:
        self.usdm = BinanceUsdm(testnet, client)
        self.coinm = BinanceCoinm(testnet, client)
        self.spot = BinanceSpot(client)

    async def get_instruments(self) -> list[Instrument]:
        async with asyncio.TaskGroup() as tg:
            usdm = tg.create_task(self.usdm.get_instruments())
            coinm = tg.create_task(self.coinm.get_instruments())
            spot = tg.create_task(self.spot.get_instruments())
        return [*usdm.result(), *coinm.result(), *spot.result()]
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

    def _get_section(self, section: Section) -> ExchangeInterface:
        return getattr(self, section.value)
