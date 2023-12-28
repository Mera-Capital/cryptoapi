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
from .constants import INVALID_CREDS_CODE
from .url import DeribitURL
from .mapping import _DERIBIT_MAPPER, _candle_converter, _position_converter
from .access import AccessToken
from ...api.exceptions import BadResponseAPIError


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

    async def get_position(self, instrument: Instrument, creds: dict[str, str]) -> Position:
        url = self._url.position.format(instrument_name=instrument.title)
        raw_result = await self.get(url, headers=await self._get_headers(creds))
        return _position_converter(raw_result, instrument)

    async def get_operations_summary(self, instrument: Instrument, creds: dict[str, str]) -> OperationsSummary:  # type: ignore[empty-body] # noqa #E501
        pass

    async def cancel_all_orders(self, instrument: Instrument, creds: dict[str, str]) -> CommandStatus:
        url = self._url.cancel_orders.format(instrument_name=instrument.title)
        raw_result = await self.get(url, headers=await self._get_headers(creds))
        return CommandStatus(success=True, payload={"number of cancelled orders": raw_result})

    async def close_position(self, instrument: Instrument, creds: dict[str, str]) -> CommandStatus:
        url = self._url.close_position.format(instrument_name=instrument.title)
        raw_result = await self.get(url, headers=await self._get_headers(creds))
        return CommandStatus(success=bool(raw_result["order"]["order_state"] == "filled"), payload=raw_result["order"])

    async def buy(
            self,
            amount: Decimal,
            order_type: OrderType,
            instrument: Instrument,
            creds: dict[str, str],
    ) -> OrderInfo:
        amount = self._round_order_amount(amount, instrument)
        url = self._url.buy.format(amount=amount, instrument_name=instrument.title, order_type=order_type.value)
        raw_result = await self.get(url, headers=await self._get_headers(creds))
        return self._mapper.load(raw_result["order"], OrderInfo)

    async def sell(
            self,
            amount: Decimal,
            order_type: OrderType,
            instrument: Instrument,
            creds: dict[str, str],
    ) -> OrderInfo:
        amount = self._round_order_amount(amount, instrument)
        url = self._url.sell.format(amount=amount, instrument_name=instrument.title, order_type=order_type.value)
        raw_result = await self.get(url, headers=await self._get_headers(creds))
        return self._mapper.load(raw_result["order"], OrderInfo)

    async def check_credentials(self, creds: dict[str, str]) -> CommandStatus:  # TODO: add tests
        client_id, client_secret, creds_key = self._parse_creds(creds)
        token = self._get_token(creds_key)
        if not token:
            try:
                token = await self._auth(client_id, client_secret)
                self._set_token(creds_key, token)
            except BadResponseAPIError as err:
                if err.error_code == INVALID_CREDS_CODE:
                    return CommandStatus(False, payload={"message": err.message})
                raise err from err
        if token and not token.scope_is_valid:
            return CommandStatus(False, payload={"message": "invalid scope"})
        return CommandStatus(True, payload={"message": "credentials is valid"})

    async def _auth(self, client_id: str, client_secret: str) -> AccessToken:
        raw_result = await self.get(self._url.auth.format(client_id=client_id, client_secret=client_secret))
        return AccessToken.create(raw_result)

    async def _get_headers(self, creds: dict[str, str]) -> dict[str, str]:
        client_id, client_secret, creds_key = self._parse_creds(creds)
        token = self._get_token(creds_key)
        if (token is not None and token.is_expire) or token is None:
            token = await self._auth(client_id, client_secret)
            self._set_token(creds_key, token)
        return {"Authorization": f"Bearer {token.access_token}", "Content-Type": "application/json"}

    def _get_token(self, creds_key: str) -> AccessToken | None:
        return self._tokens_store.get(creds_key)

    def _set_token(self, creds_key: str, token: AccessToken) -> None:
        self._tokens_store[creds_key] = token

    @staticmethod
    def _parse_creds(creds: dict[str, str]) -> tuple[str, str, str]:
        client_id, client_secret = creds["client_id"], creds["client_secret"]
        creds_key = client_id + client_secret
        return client_id, client_secret, creds_key

    @staticmethod
    def _round_order_amount(amount: Decimal, instrument: Instrument) -> Decimal:
        if instrument.is_direct:
            return amount.quantize(Decimal('1.00'))  # TODO: make rounding for all currencies
        return (amount / instrument.min_trade_amount * instrument.min_trade_amount).quantize(Decimal('1.00'))
