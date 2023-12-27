import json
from typing import Any

import websockets

from cryptoapi.api.protocols.clients import WSSClientProtocol


class BaseWSSClient(WSSClientProtocol):
    def __init__(self, wsuri: str) -> None:
        """
        Initializes the BaseWSSClient instance.
        :param wsuri: The WebSocket URI.
        :return: None
        """
        self._wsuri = wsuri
        self.websocket: None | websockets.WebSocketClientProtocol = None

    async def subscribe(self, msg: dict[str, Any]) -> None:
        """
        Subscribes from a specific channel.
        :param msg: The message to send to the websocket.
        :return: None
        """
        websocket = await self.connect()
        await websocket.send(json.dumps(msg))

    async def unsubscribe(self, msg: dict[str, Any]) -> None:
        """
        Unsubscribes from a specific channel.
        :param msg: The message to send to the websocket.
        :return: None
        """
        websocket = await self.connect()
        await websocket.send(msg)

    async def unsubscribe_all(self, msg: dict[str, Any]) -> None:
        """
        Unsubscribes from all channels.
        :param msg: The message to send to the websocket.
        :return: None
        """
        websocket = await self.connect()
        await websocket.send(json.dumps(msg))

    async def connect(self) -> websockets.WebSocketClientProtocol:
        """
        Socket manager
        :return WebSocketClientProtocol: Current or new socket instance
        """
        if self.websocket is None or self.websocket.open is False:
            self.websocket = await self._create_websocket()
        return self.websocket

    async def close(self) -> None:
        """
        Closes the websocket connection if it exists.
        :return: None
        """
        websocket = await self.connect()
        if websocket:
            await websocket.close()

    async def _create_websocket(self) -> websockets.WebSocketClientProtocol:
        """
        Socket builder
        :return WebSocketClientProtocol: New socket instance
        """
        return await websockets.connect(self._wsuri)

    async def __aenter__(self) -> 'BaseWSSClient':
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
