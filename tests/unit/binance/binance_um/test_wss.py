from decimal import Decimal
from typing import Coroutine

import pytest
from _pytest.monkeypatch import MonkeyPatch

from cryptoapi.api.entities import ClosedTimeframeEvent, Timeframe, Candle
from cryptoapi.exchanges.binance.usdm.wss import WSSBinanceUMClient
from tests.unit.binance.binance_um.mock import MockListenCoro

REFERENCE_LISTEN = ClosedTimeframeEvent(
    timeframe=Timeframe.M1,
    instrument_title='BTCUSDT',
    candle=Candle(
        timestamp=1704885239999,
        open=Decimal("46481.20"),
        high=Decimal("46749.00"),
        low=Decimal("46481.20"),
        close=Decimal("46677.40")
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
        wss_binance_um: WSSBinanceUMClient,
        mock_coro: Coroutine,
        reference: None | ClosedTimeframeEvent,
) -> None:
    # Arrange
    monkeypatch.setattr(WSSBinanceUMClient, "listen_socket", mock_coro)
    # Act
    result = await wss_binance_um.listen()
    # Assert
    assert result == reference


def test_create_message(wss_binance_um: WSSBinanceUMClient) -> None:
    result = wss_binance_um.create_message_for_chart_data("BTCUSDT", 1)
    assert result == {'method': 'SUBSCRIBE', 'params': ['btcusdt@kline_1m'], 'id': 1}
