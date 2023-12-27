import json

from cryptoapi.clients.wss.base import BaseWSSClient


async def test_connect_ws() -> None:
    # Arrange
    wsuri = 'wss://dstream.binance.com/ws/btcusd_200925@aggTrade'
    MSG = {
        "method": "SUBSCRIBE",
        "params":
            [
                "btcusd_perp@aggTrade",
            ],
        "id": 1
    }
    client = BaseWSSClient(wsuri)
    await client.subscribe(MSG)
    ws = await client.get_websocket()
    # Act
    response = json.loads(await ws.recv())
    # Assert
    assert response.get('id') == MSG.get('id')
