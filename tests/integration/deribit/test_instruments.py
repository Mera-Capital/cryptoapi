from aioresponses import aioresponses

from cryptoapi.clients.http import BaseHTTPClient
from cryptoapi.exchanges.deribit import Deribit


async def test_instruments(server_mock: "aioresponses") -> None:
    server_mock.stop()
    async with BaseHTTPClient() as client:
        deribit = Deribit(True, client)
        result = await deribit.get_instruments()
        print(result)
