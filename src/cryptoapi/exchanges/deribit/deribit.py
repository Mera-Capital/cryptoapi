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
from .mapping import _DERIBIT_MAPPER, _candle_converter
from .access import AccessToken


class Deribit(DeribitClient, ExchangeInterface):
    def __init__(self, testnet: bool, client: HTTPClientInterface) -> None:
        super().__init__(client)
        self._url = DeribitURL(testnet)
        self._mapper = _DERIBIT_MAPPER
        self._tokens_store: dict[str, AccessToken] = {}

    async def get_instruments(self) -> list[Instrument]:
        async with asyncio.TaskGroup() as tg:
            btc = tg.create_task(self.get(self._url.instruments.format(currency="BTC")))
            eth = tg.create_task(self.get(self._url.instruments.format(currency="ETH")))
            usdc = tg.create_task(self.get(self._url.instruments.format(currency="USDC")))
            usdt = tg.create_task(self.get(self._url.instruments.format(currency="USDT")))
        raw_result, instruments = [*btc.result(), *eth.result(), *usdc.result(), *usdt.result()], []
        for raw in raw_result:
            instrument = self._mapper.load({"section": Section.MAIN, "model": raw}, Instrument)
            instruments.append(instrument)
        return instruments

    async def get_candles(
            self,
            instrument_title: str,
            section: Section,
            timeframe: Timeframe,
            date_from: int,
            date_to: int,
    ) -> list[Candle]:
        url = self._url.candles.format(
            instrument_name=instrument_title,
            resolution=timeframe.value,
            start_timestamp=date_from,
            end_timestamp=date_to,
        )
        raw_result = await self.get(url)
        return _candle_converter(raw_result)

    async def get_quotes(self, instrument_title: str, section: Section) -> Quotes:
        raw_result = await self.get(self._url.quotes.format(instrument_name=instrument_title))
        return self._mapper.load(raw_result, Quotes)

    async def get_index_price(self, currency_pair: str, section: Section) -> CurrencyIndexPrice:
        raw_result = await self.get(self._url.index_price.format(index_name=currency_pair))
        return self._mapper.load(raw_result, CurrencyIndexPrice)

    async def get_equity(self, currency: str, section: Section, creds: dict[str, str]) -> Equity:
        raw_result = await self.get(self._url.equity.format(currency=currency), headers=await self._get_headers(creds))
        return self._mapper.load(raw_result, Equity)

    async def get_position(self, instrument: Instrument, creds: dict[str, str]) -> Position:  # type: ignore[empty-body]
        pass

    async def get_operations_summary(self, instrument: Instrument, creds: dict[str, str]) -> OperationsSummary:  # type: ignore[empty-body] # noqa #E501
        pass

    async def cancel_all_orders(self, instrument: Instrument, creds: dict[str, str]) -> CommandStatus:  # type: ignore[empty-body] # noqa #E501
        pass

    async def close_position(self, instrument: Instrument, creds: dict[str, str]) -> CommandStatus:  # type: ignore[empty-body] # noqa #E501
        pass

    async def buy(  # type: ignore[empty-body]
            self,
            amount: Decimal,
            order_type: OrderType,
            instrument: Instrument,
            creds: dict[str, str],
    ) -> OrderInfo:
        pass

    async def sell(  # type: ignore[empty-body]
            self,
            amount: Decimal,
            order_type: OrderType,
            instrument: Instrument,
            creds: dict[str, str],
    ) -> OrderInfo:
        pass

    async def check_credentials(self, creds: dict[str, str]) -> CommandStatus:  # type: ignore[empty-body]
        pass

    async def _auth(self, client_id: str, client_secret: str) -> AccessToken:
        raw_result = await self.get(self._url.auth.format(client_id=client_id, client_secret=client_secret))
        return AccessToken.create(raw_result)

    async def _get_headers(self, creds: dict[str, str]) -> dict[str, str]:
        client_id, client_secret = creds["client_id"], creds["client_secret"]
        creds_key = client_id + client_secret
        token = self._tokens_store.get(creds_key)
        if (token is not None and token.is_expire) or token is None:
            token = await self._auth(client_id, client_secret)
            self._tokens_store[creds_key] = token
        return {"Authorization": f"Bearer {token.access_token}", "Content-Type": "application/json"}
