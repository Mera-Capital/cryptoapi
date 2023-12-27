import pytest_asyncio

from cryptoapi.clients.http import BaseHTTPClient
from cryptoapi.exchanges.deribit import Deribit


@pytest_asyncio.fixture
async def deribit() -> Deribit:
    client = BaseHTTPClient()
    yield Deribit(True, client)
    await client.close()
