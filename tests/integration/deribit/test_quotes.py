from decimal import Decimal

from cryptoapi.api.entities import Section, Quotes
from cryptoapi.exchanges.deribit import Deribit
from tests.mocks import MockServer


async def test_quotes(deribit: Deribit, server_mock: MockServer) -> None:
    # Arrange
    expected = Quotes(index_price=Decimal("42900.0"), markup_price=Decimal("42934.92"), timestamp=1703767036555)
    url = deribit._url.quotes.format(instrument_name="BTC-PERPETUAL")
    server_mock.get(url, payload=server_mock.load("deribit", "ticker_btc_perpetual"))
    # Act
    quotes = await deribit.get_quotes("BTC-PERPETUAL", Section.MAIN)
    # Assert
    assert expected == quotes
