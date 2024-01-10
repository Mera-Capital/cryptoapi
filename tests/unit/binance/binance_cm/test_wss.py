from decimal import Decimal
from typing import Coroutine

import pytest
from _pytest.monkeypatch import MonkeyPatch

from cryptoapi.api.entities import ClosedTimeframeEvent, Timeframe, Candle
from cryptoapi.exchanges.binance.coinm.wss import WSSBinanceCMClient
from tests.unit.binance.binance_cm.mock import MockListenCoro

REFERENCE_LISTEN = ClosedTimeframeEvent(
    timeframe=Timeframe.M1,
    instrument_title='BTCUSD_PERP',
    candle=Candle(
        timestamp=1704886319999,
        open=Decimal("45601.3"),
        high=Decimal("49799.9"),
        low=Decimal("45601.3"),
        close=Decimal("49799.9")
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
        wss_binance_cm: WSSBinanceCMClient,
        mock_coro: Coroutine,
        reference: None | ClosedTimeframeEvent,
) -> None:
    # Arrange
    monkeypatch.setattr(WSSBinanceCMClient, "listen_socket", mock_coro)
    # Act
    result = await wss_binance_cm.listen()
    print(result)
    # Assert
    assert result == reference


def test_create_message(wss_binance_cm: WSSBinanceCMClient) -> None:
    result = wss_binance_cm.create_message_for_chart_data("BTCUSDT", 1)
    assert result == {"method": "SUBSCRIBE", "params": ["btcusdt@kline_1m"], "id": 1}
