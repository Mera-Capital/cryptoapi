import json

from cryptoapi.clients.wss import BaseWSSClient


async def test_connect_ws() -> None:
    # Arrange
    wsuri = "wss://dstream.binance.com/ws/btcusd_200925@aggTrade"
    msg = {"method": "SUBSCRIBE", "params": ["btcusd_perp@aggTrade"], "id": 1}
    # Act
    async with BaseWSSClient(wsuri) as client:
        await client.subscribe(msg)
        ws = await client._get_socket()
        response = json.loads(await ws.recv())
    # Assert
    assert response.get("id") == msg.get("id")