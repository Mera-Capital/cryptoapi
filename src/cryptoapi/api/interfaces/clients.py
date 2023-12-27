from typing import Protocol, Any
from abc import abstractmethod

from aiohttp.typedefs import StrOrURL


class HTTPClientInterface(Protocol):
    @abstractmethod
    async def get(
            self,
            url: StrOrURL,
            headers: dict[str, Any] | None = None,
    ) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def post(
            self,
            url: StrOrURL,
            body: dict[str, Any] | None = None,
            headers: dict[str, Any] | None = None,
    ) -> Any:
        raise NotImplementedError
