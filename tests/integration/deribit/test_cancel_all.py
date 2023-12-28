from cryptoapi.api.entities import CommandStatus
from cryptoapi.exchanges.deribit import Deribit
from tests.integration.deribit.fixtures import BTC_PERPETUAL_CORRECT
from tests.mocks import MockServer


async def test_cancel_all(deribit: Deribit, server_mock: MockServer) -> None:
    # Arrange
    expected = CommandStatus(success=True, payload={"number of cancelled orders": 0})
    creds = {"client_id": "client_id", "client_secret": "client_secret"}
    url = deribit._url.cancel_orders.format(instrument_name=BTC_PERPETUAL_CORRECT.title)
    server_mock.get(url, payload=server_mock.load("deribit", "cancel_all_btc_perpetual"))
    # Act
    result = await deribit.cancel_all_orders(BTC_PERPETUAL_CORRECT, creds)
    # Assert
    assert result == expected
