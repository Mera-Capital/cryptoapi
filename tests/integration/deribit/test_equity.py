from decimal import Decimal

from cryptoapi.api.entities import Section, Equity
from cryptoapi.exchanges.deribit import Deribit
from tests.mocks import MockServer


async def test_equity(deribit: Deribit, server_mock: MockServer) -> None:
    # Arrange
    expected = Equity(size=Decimal("68.09698847"))
    creds = {"client_id": "client_id", "client_secret": "client_secret"}
    url = deribit._url.equity.format(currency="BTC")
    server_mock.get(url, payload=server_mock.load("deribit", "equity_btc"))
    # Act
    equity = await deribit.get_equity("BTC", Section.MAIN, creds)
    # Assert
    assert equity == expected
