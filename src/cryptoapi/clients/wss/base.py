import json
from time import sleep
from types import TracebackType
from typing import Any, Type

import websockets

from cryptoapi.api.interfaces import WSSClientInterface


class BaseWSSClient(WSSClientInterface):

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

    async def listen_socket(self) -> Any:
        """
        Listens to the socket and returns the received JSON data.
        :param self: The current instance of the class.
        :return: The received JSON data.
        """
        socket = await self._get_socket()
        return json.loads(await socket.recv())

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

    async def __aenter__(self) -> "BaseWSSClient":
        await self._get_socket()
        return self

    async def __aexit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> None:
        await self.close()

    async def __anext__(self) -> "BaseWSSClient":
        return self

    def __aiter__(self) -> "BaseWSSClient":
        sleep(10)
        return self
