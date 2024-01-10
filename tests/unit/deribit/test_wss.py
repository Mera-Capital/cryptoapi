from decimal import Decimal
from typing import Coroutine

import pytest
from _pytest.monkeypatch import MonkeyPatch

from cryptoapi.api.entities import ClosedTimeframeEvent, Timeframe, Candle
from cryptoapi.exchanges.deribit.wss import WSSDeribitClient
from tests.unit.deribit.mock import MockListenCoro

REFERENCE_LISTEN = ClosedTimeframeEvent(
    timeframe=Timeframe.M1,
    instrument_title="BTC-PERPETUAL",
    candle=Candle(
        timestamp=1704882960000,
        open=Decimal("45657"),
        high=Decimal("45657"),
        low=Decimal("45642.5"),
        close=Decimal("45643.5")
    ))


@pytest.mark.parametrize(
    "mock_coro, reference",
    [
        (MockListenCoro.is_response, REFERENCE_LISTEN),
        (MockListenCoro.is_not_response, None)
    ]
)
async def test_listen(
        monkeypatch: MonkeyPatch,
        wss_deribit: WSSDeribitClient,
        mock_coro: Coroutine,
        reference: None | ClosedTimeframeEvent,
) -> None:
    # Arrange
    monkeypatch.setattr(WSSDeribitClient, "listen_socket", mock_coro)
    # Act
    result = await wss_deribit.listen()
    # Assert
    assert result == reference


def test_create_message(wss_deribit: WSSDeribitClient) -> None:
    result = wss_deribit.create_message_for_chart_data("BTC-PERPETUAL", 1)
    assert result == {
        "jsonrpc": "2.0",
        "method": "public/subscribe",
        "params": {
            "channels": ["chart.trades.BTC-PERPETUAL.1"]
        }
    }
