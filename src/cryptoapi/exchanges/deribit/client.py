from typing import Any, Protocol
from abc import abstractmethod

from aiohttp.typedefs import StrOrURL

from cryptoapi.api.exceptions import BadResponseAPIError, TimeoutAPIError
from cryptoapi.api.interfaces import HTTPClientInterface
from cryptoapi.clients.http import HTTPClientError


class DeribitJRPCInterface(Protocol):
    @abstractmethod
    async def get(
            self,
            url: StrOrURL,
            headers: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        raise NotImplementedError


class DeribitClient(DeribitJRPCInterface):
    def __init__(self, client: HTTPClientInterface) -> None:
        self._client = client

    async def get(self, url: StrOrURL, headers: dict[str, Any] | None = None) -> dict[str, Any]:
        try:
            payload = await self._client.get(url, headers=headers)
            return payload["result"]  # type: ignore[no-any-return]
        except HTTPClientError as err:
            error = err.payload.get("error", {"message": "unknown", "code": 0})
            raise BadResponseAPIError(message=error["message"], error_code=error["code"]) from err
        except TimeoutError as err:
            raise TimeoutAPIError() from err
