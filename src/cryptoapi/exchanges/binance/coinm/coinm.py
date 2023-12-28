from decimal import Decimal

from cryptoapi.api.interfaces import HTTPClientInterface
from cryptoapi.exchanges.binance.client import BinanceClient
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
    OrderInfo, Kind
)
from .url import CoinmURL
from .mapping import _COINM_MAPPER


class BinanceCoinm(BinanceClient, ExchangeInterface):
    def __init__(self, testnet: bool, client: HTTPClientInterface):
        super().__init__(client)
        self._url = CoinmURL(testnet)
        self._mapper = _COINM_MAPPER

    async def get_instruments(self) -> list[Instrument]:
        raw_result = await self.get(self._url.instruments)
        return [self._mapper.load(
            {
                "section": Section.COINM,
                "kind": Kind.FUTURE,
                "active_status": True,
                "min_trade_amount": Decimal(str(instrument["contractSize"])),
                "model": instrument}, Instrument
        ) for instrument in raw_result["symbols"]]

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