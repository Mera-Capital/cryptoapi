from decimal import Decimal

from cryptoapi.api.entities import Section, CurrencyIndexPrice
from cryptoapi.exchanges.deribit import Deribit
from tests.mocks import MockServer


async def test_index_price(deribit: Deribit, server_mock: MockServer) -> None:
    # Arrange
    expected = CurrencyIndexPrice(index_price=Decimal("42839.3"))
    url = deribit._url.index_price.format(index_name="btc_usd")
    server_mock.get(url, payload=server_mock.load("deribit", "index_price_btc_usd"))
    # Act
    index_price = await deribit.get_index_price("btc_usd", Section.MAIN)
    # Assert
    assert expected == index_price
