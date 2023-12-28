from decimal import Decimal

import pytest

from cryptoapi.api.entities import Section, Position, Instrument
from cryptoapi.exchanges.deribit import Deribit
from tests.integration.deribit.fixtures import BTC_PERPETUAL_CORRECT, BTC_PERPETUAL_IS_DIRECT
from tests.mocks import MockServer


@pytest.mark.parametrize("instrument, expected", [
    (BTC_PERPETUAL_CORRECT, Position(size=Decimal("1567300"))),
    (BTC_PERPETUAL_IS_DIRECT, Position(size=Decimal("37.003581129"))),
])
async def test_position(deribit: Deribit, server_mock: MockServer, instrument: Instrument, expected: Position) -> None:
    # Arrange
    creds = {"client_id": "client_id", "client_secret": "client_secret"}
    url = deribit._url.position.format(instrument_name=instrument.title)
    server_mock.get(url, payload=server_mock.load("deribit", "position_btc_perpetual"))
    # Act
    position = await deribit.get_position(instrument, creds)
    # Assert
    assert expected == position
