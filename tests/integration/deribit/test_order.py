from decimal import Decimal

from cryptoapi.api.entities import OrderType, OrderInfo, OrderState, OrderDirection
from cryptoapi.exchanges.deribit import Deribit
from tests.integration.deribit.fixtures import BTC_PERPETUAL_CORRECT
from tests.mocks import MockServer


async def test_buy(deribit: Deribit, server_mock: MockServer) -> None:
    # Arrange
    expected = OrderInfo(
        instrument_title="BTC-PERPETUAL",
        average_price=Decimal("37774.05"),
        original_amount=Decimal("10.00"),
        executed_amount=Decimal("10.00"),
        state=OrderState.FILLED,
        direction=OrderDirection.BUY,
        type=OrderType.MARKET,
    )
    creds = {"client_id": "client_id", "client_secret": "client_secret"}
    url = deribit._url.buy.format(
        amount=Decimal("10.00"),
        instrument_name=BTC_PERPETUAL_CORRECT.title,
        order_type=OrderType.MARKET.value,
    )
    server_mock.get(url, payload=server_mock.load("deribit", "buy_btc_perpetual"))
    # Act
    order = await deribit.buy(Decimal("10.00"), OrderType.MARKET, BTC_PERPETUAL_CORRECT, creds)
    # Assert
    assert expected == order


async def test_sell(deribit: Deribit, server_mock: MockServer) -> None:
    # Arrange
    expected = OrderInfo(
        instrument_title="BTC-PERPETUAL",
        average_price=Decimal("37773.48"),
        original_amount=Decimal("10.00"),
        executed_amount=Decimal("10.00"),
        state=OrderState.FILLED,
        direction=OrderDirection.SELL,
        type=OrderType.MARKET,
    )
    creds = {"client_id": "client_id", "client_secret": "client_secret"}
    url = deribit._url.sell.format(
        amount=Decimal("10.00"),
        instrument_name=BTC_PERPETUAL_CORRECT.title,
        order_type=OrderType.MARKET.value,
    )
    server_mock.get(url, payload=server_mock.load("deribit", "sell_btc_perpetual"))
    # Act
    order = await deribit.sell(Decimal("10.00"), OrderType.MARKET, BTC_PERPETUAL_CORRECT, creds)
    # Assert
    assert expected == order
