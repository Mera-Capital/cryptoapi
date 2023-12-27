from typing import Any

from aiohttp import ClientResponseError, ClientResponse


class HTTPClientError(ClientResponseError):
    def __init__(self, response: ClientResponse, payload: dict[str, Any]) -> None:
        super().__init__(
            request_info=response.request_info,
            history=response.history,
            status=response.status,
            headers=response.headers,
        )
        self.payload = payload
