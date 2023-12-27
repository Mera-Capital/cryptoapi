import json
from typing import Any

import websockets

from cryptoapi.api.protocols.clients import WSSClientProtocol


class BaseWSSClient(WSSClientProtocol):
    def __init__(self, uri: str) -> None:
        """
        Initializes the BaseWSSClient instance.
        :param uri: The WebSocket URI.
        :return: None
        """
        self._uri = uri
        self.socket: None | websockets.WebSocketClientProtocol = None

    async def subscribe(self, msg: dict[str, Any]) -> None:
        """
        Subscribes from a specific channel.
        :param msg: The message to send to the websocket.
        :return: None
        """
        socket = await self._get_socket()
        await socket.send(json.dumps(msg))

    async def unsubscribe(self, msg: dict[str, Any]) -> None:
        """
        Unsubscribes from a specific channel.
        :param msg: The message to send to the websocket.
        :return: None
        """
        socket = await self._get_socket()
        await socket.send(json.dumps(msg))

    async def unsubscribe_all(self, msg: dict[str, Any]) -> None:
        """
        Unsubscribes from all channels.
        :param msg: The message to send to the websocket.
        :return: None
        """
        socket = await self._get_socket()
        await socket.send(json.dumps(msg))

    async def close(self) -> None:
        """
        Closes the websocket connection if it exists.
        :return: None
        """
        socket = await self._get_socket()
        if socket:
            await socket.close()

    async def _get_socket(self) -> websockets.WebSocketClientProtocol:
        """
        Socket manager
        :return WebSocketClientProtocol: Current or new socket instance
        """
        if self.socket is None or self.socket.open is False:
            self.socket = await self._create_socket()
        return self.socket

    async def _create_socket(self) -> websockets.WebSocketClientProtocol:
        """
        Socket builder
        :return WebSocketClientProtocol: New socket instance
        """
        return await websockets.connect(self._uri)

    async def __aenter__(self) -> 'BaseWSSClient':
        await self._get_socket()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
