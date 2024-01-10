import pytest

from cryptoapi.exchanges.deribit.wss import WSSDeribitClient


@pytest.fixture(scope="session")
def wss_deribit() -> WSSDeribitClient:
    return WSSDeribitClient(True)
