from typing import Any, Protocol, TypeVar

T = TypeVar("T")


class MapperInterface(Protocol):
    def load(self, data: Any, class_: type[T]) -> T:
        raise NotImplementedError

    def dump(self, data: Any) -> dict[str, Any]:
        raise NotImplementedError
