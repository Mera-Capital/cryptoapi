import pytest

from cryptoapi.clients.http import BaseHTTPClient, BaseHTTPClientError


async def test_success_response() -> None:
    client = BaseHTTPClient()
    payload = await client.get("https://test.deribit.com/api/v2/public/get_index_price?index_name=ada_usd")
    assert payload["jsonrpc"] == "2.0"


async def test_base_error() -> None:
    client = BaseHTTPClient()
    with pytest.raises(BaseHTTPClientError):
        await client.get("https://test.deribit.com/api/v2/public/get_index_price?index_name=error")
