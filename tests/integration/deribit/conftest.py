import pytest
import pytest_asyncio

from cryptoapi.clients.http import BaseHTTPClient
from cryptoapi.exchanges.deribit import Deribit
from tests.mocks import MockServer


@pytest_asyncio.fixture
async def deribit() -> Deribit:
    client = BaseHTTPClient()
    yield Deribit(True, client)
    await client.close()


@pytest.fixture(autouse=True)
def setup_auth(deribit: Deribit, server_mock: MockServer) -> None:
    url = ("https://test.deribit.com/api/v2/public/auth?"
           "client_id=client_id&client_secret=client_secret&grant_type=client_credentials")
    server_mock.get(url, payload=server_mock.load("deribit", "auth_success"))
