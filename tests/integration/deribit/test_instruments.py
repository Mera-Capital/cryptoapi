from decimal import Decimal

from cryptoapi.api.entities import Instrument, Section, Kind
from cryptoapi.exchanges.deribit import Deribit
from tests.mocks import MockServer


async def test_instruments(deribit: Deribit, server_mock: MockServer) -> None:
    # Arrange
    expected_len = 39
    expected_last = Instrument(
        title="ETH_USDT-PERPETUAL",
        section=Section.MAIN,
        underlying_currency="ETH",
        margin_currency="USDT",
        quoted_currency="USDT",
        contract_size=Decimal("0.01"),
        min_trade_amount=Decimal("0.01"),
        kind=Kind.FUTURE,
        active_status=True,
        creation_timestamp=1702245256000,
    )
    url = deribit._url.instruments
    server_mock.get(url.format(currency="BTC"), payload=server_mock.load("deribit", "instruments_btc"))
    server_mock.get(url.format(currency="ETH"), payload=server_mock.load("deribit", "instruments_eth"))
    server_mock.get(url.format(currency="USDT"), payload=server_mock.load("deribit", "instruments_usdt"))
    server_mock.get(url.format(currency="USDC"), payload=server_mock.load("deribit", "instruments_usdc"))
    # Act
    instruments = await deribit.get_instruments()
    # Assert
    assert len(instruments) == expected_len
    assert instruments[-1] == expected_last
