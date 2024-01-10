from cryptoapi.api.entities import CommandStatus
from cryptoapi.exchanges.deribit import Deribit
from tests.integration.deribit.fixtures import BTC_PERPETUAL_CORRECT
from tests.mocks import MockServer


async def test_close_position(deribit: Deribit, server_mock: MockServer) -> None:
    # Arrange
    expected = CommandStatus(
        success=True,
        payload={
            "is_liquidation": False,
            "risk_reducing": False,
            "order_type": "market",
            "creation_timestamp": 1703785099522,
            "order_state": "filled",
            "filled_amount": 1567300,
            "average_price": 42607.33,
            "order_id": "20561666639",
            "reduce_only": True,
            "last_update_timestamp": 1703785099522,
            "post_only": False,
            "replaced": False,
            "web": False,
            "api": True,
            "max_show": 1567300,
            "time_in_force": "good_til_cancelled",
            "direction": "sell",
            "mmp": False,
            "instrument_name": "BTC-PERPETUAL",
            "amount": 1567300,
            "price": 42002,
            "label": ""},
    )
    creds = {"client_id": "client_id", "client_secret": "client_secret"}
    url = deribit._url.close_position.format(instrument_name=BTC_PERPETUAL_CORRECT.title)
    server_mock.get(url, payload=server_mock.load("deribit", "close_position_btc_perpetual"))
    # Act
    result = await deribit.close_position(BTC_PERPETUAL_CORRECT, creds)
    # Assert
    assert result == expected
