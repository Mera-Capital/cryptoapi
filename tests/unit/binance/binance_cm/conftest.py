import pytest

from cryptoapi.exchanges.binance.coinm.wss import WSSBinanceCMClient


@pytest.fixture(scope="session")
def wss_binance_cm() -> WSSBinanceCMClient:
    return WSSBinanceCMClient(True)
