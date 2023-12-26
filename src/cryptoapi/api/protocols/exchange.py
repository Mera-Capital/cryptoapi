from abc import abstractmethod
from decimal import Decimal
from typing import Protocol

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


class ExchangeProtocol(Protocol):
    # Public methods
    @abstractmethod
    async def get_instruments(self) -> list[Instrument]:
        raise NotImplementedError

    @abstractmethod
    async def get_candles(
            self,
            instrument_title: str,
            section: Section,
            timeframe: Timeframe,
            date_from: int,
            date_to: int,
    ) -> list[Candle]:
        raise NotImplementedError

    @abstractmethod
    async def get_quotes(self, instrument_title: str, section: Section) -> Quotes:
        raise NotImplementedError

    @abstractmethod
    async def get_index_price(self, currency_pair: str, section: Section) -> CurrencyIndexPrice:
        raise NotImplementedError

    # Private methods
    @abstractmethod
    async def get_position(self, instrument: Instrument, creds: dict[str, str]) -> Position:
        raise NotImplementedError

    @abstractmethod
    async def get_equity(self, instrument: Instrument, creds: dict[str, str]) -> Equity:
        raise NotImplementedError

    @abstractmethod
    async def get_operations_summary(self, instrument: Instrument, creds: dict[str, str]) -> OperationsSummary:
        raise NotImplementedError

    @abstractmethod
    async def cancel_all_orders(self, instrument: Instrument, creds: dict[str, str]) -> CommandStatus:
        raise NotImplementedError

    @abstractmethod
    async def close_position(self, instrument: Instrument, creds: dict[str, str]) -> CommandStatus:
        raise NotImplementedError

    @abstractmethod
    async def buy(
            self,
            amount: Decimal,
            order_type: OrderType,
            instrument: Instrument,
            creds: dict[str, str]
    ) -> OrderInfo:
        raise NotImplementedError

    @abstractmethod
    async def sell(
            self,
            amount: Decimal,
            order_type: OrderType,
            instrument: Instrument,
            creds: dict[str, str]
    ) -> OrderInfo:
        raise NotImplementedError

    @abstractmethod
    async def check_credentials(self, instrument: Instrument, creds: dict[str, str]) -> CommandStatus:
        raise NotImplementedError
