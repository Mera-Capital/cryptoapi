import json
from typing import Any

import websockets
from websockets import WebSocketClientProtocol

from cryptoapi.api.protocols.clients import WSSClientProtocol


class BaseWSSClient(WSSClientProtocol):
    def __init__(self, wsuri: str) -> None:
        self._wsuri = wsuri
        self.websocket: None | WebSocketClientProtocol = None

    async def subscribe(self, msg: dict[str, Any]) -> None:
        websocket = await self.get_websocket()
        await websocket.send(json.dumps(msg))

    async def unsubscribe(self, msg: dict[str, Any]) -> None:
        websocket = await self.get_websocket()
        await websocket.send(msg)

    async def unsubscribe_all(self, msg: dict[str, Any]) -> None:
        websocket = await self.get_websocket()
        await websocket.send(json.dumps(msg))

    async def get_websocket(self) -> WebSocketClientProtocol:
        if self.websocket is None or self.websocket.open is False:
            self.websocket = await self._create_websocket()
        return self.websocket

    async def _create_websocket(self) -> WebSocketClientProtocol:
        return await websockets.connect(self._wsuri)
