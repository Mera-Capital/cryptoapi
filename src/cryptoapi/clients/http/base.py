import ssl
from types import TracebackType
from typing import Any, Type

import certifi
from aiohttp import ClientSession, TCPConnector, ClientTimeout
from aiohttp.typedefs import StrOrURL

from cryptoapi.api.protocols import HTTPClientProtocol
from .exceptions import BaseHTTPClientError


class BaseHTTPClient(HTTPClientProtocol):
    def __init__(
            self,
            timeout: int | None = None,
            connection_limit: int = 0,
    ) -> None:
        """
        :param timeout: Total number of seconds for the whole request, use None for disable timeout
        :param connection_limit: Total number simultaneous connections, use 0 for disable limit
        :return: None
        """

        self._ssl_context = ssl.create_default_context(cafile=certifi.where())
        self._connector = TCPConnector(ssl=self._ssl_context, limit=connection_limit)
        self._timeout = ClientTimeout(total=timeout)
        self._session = self._create_session()
        self.ok_status = 200

    def _get_session(self) -> ClientSession:
        """
        Session manager
        :return ClientSession: Current or new session instance
        """
        if not self._session.closed:
            return self._session
        self._session = self._create_session()
        return self._session

    def _create_session(self) -> ClientSession:
        """
        Session builder
        :return ClientSession: New session instance
        """
        return ClientSession(connector=self._connector, timeout=self._timeout)

    async def get(
            self,
            url: StrOrURL,
            headers: dict[str, Any] | None = None,
    ) -> Any:
        """
        Closes current session
        :param url: URL to GET request
        :param headers: Optional headers
        :return Any: JSON payload
        """
        async with self._get_session().get(url, headers=headers) as response:
            payload = await response.json()
            if response.status != self.ok_status:
                raise BaseHTTPClientError(response, payload)
            return payload

    async def post(
            self,
            url: StrOrURL,
            body: dict[str, Any] | None = None,
            headers: dict[str, Any] | None = None,
    ) -> Any:
        """
        Closes current session
        :param url: URL to POST request
        :param body: Optional payload
        :param headers: Optional headers
        :return Any: JSON payload
        """
        async with self._get_session().post(url, data=body, headers=headers) as response:
            payload = await response.json()
            if response.status != self.ok_status:
                raise BaseHTTPClientError(response, payload)
            return payload

    async def close(self) -> None:
        """
        Close current session
        :return None:
        """
        if not self._session.closed:
            await self._session.close()
        await self._connector.close()

    async def __aenter__(self) -> "BaseHTTPClient":
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()
