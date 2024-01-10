import pytest

from cryptoapi.exchanges.binance.usdm.wss import WSSBinanceUMClient


@pytest.fixture(scope="session")
def wss_binance_um() -> WSSBinanceUMClient:
    return WSSBinanceUMClient(True)
