from abc import abstractmethod
from typing import Protocol, Any

from aiohttp.typedefs import StrOrURL


class HTTPClientProtocol(Protocol):
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


class WSSClientProtocol(Protocol):
    @abstractmethod
    async def subscribe(self, msg: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def unsubscribe(self, msg: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def unsubscribe_all(self, msg: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError
