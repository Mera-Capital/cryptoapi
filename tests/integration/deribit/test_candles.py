from decimal import Decimal

from cryptoapi.api.entities import Candle, Section, Timeframe
from cryptoapi.exchanges.deribit import Deribit
from tests.mocks import MockServer


async def test_instruments(deribit: Deribit, server_mock: MockServer) -> None:
    # Arrange
    expected_len = 790
    expected_last = Candle(
        timestamp=1703716200000,
        open=Decimal("43550.0"),
        high=Decimal("43581.5"),
        low=Decimal("43388.0"),
        close=Decimal("43388.0"),
    )
    url = deribit._url.candles.format(
        instrument_name="BTC-PERPETUAL",
        resolution=15,
        start_timestamp=1703006836000,
        end_timestamp=1703716836000,
    )
    server_mock.get(url, payload=server_mock.load("deribit", "tradingview_chart_data_btc_perpetual"))
    # Act
    candles = await deribit.get_candles(
        "BTC-PERPETUAL",
        Section.MAIN,
        Timeframe.M15,
        1703006836000,
        1703716836000,
    )
    # Assert
    assert len(candles) == expected_len
    assert candles[-1] == expected_last
