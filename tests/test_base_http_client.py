import pytest
from aioresponses import aioresponses

from cryptoapi.clients.http import BaseHTTPClient, HTTPClientError


async def test_get_success_response(server_mock: "aioresponses") -> None:
    # Arrange
    expected_payload = {"status": "success"}
    server_mock.get("https://example.com", payload=expected_payload, status=200)
    # Act
    async with BaseHTTPClient() as client:
        payload = await client.get("https://example.com")
        # Assert
        assert payload == expected_payload


async def test_post_success_response(server_mock: "aioresponses") -> None:
    # Arrange
    expected_payload = {"status": "success"}
    server_mock.post("https://example.com", payload=expected_payload, status=200)
    # Act
    async with BaseHTTPClient() as client:
        payload = await client.post("https://example.com")
        # Assert
        assert payload == expected_payload


async def test_base_error(server_mock: "aioresponses") -> None:
    server_mock.get("https://example.com", payload={"status": "error"}, status=400)
    with pytest.raises(HTTPClientError):
        async with BaseHTTPClient() as client:
            await client.get("https://example.com")
