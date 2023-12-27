from typing import Any, TypeVar

from adaptix import Retort

from cryptoapi.api.internal import MapperProtocol
from cryptoapi.api.exceptions import MappingError

T = TypeVar("T")


class Mapper(MapperProtocol):
    def __init__(self, retort: Retort) -> None:
        self._retort = retort

    def load(self, data: Any, class_: type[T]) -> T:
        try:
            return self._retort.load(data, class_)
        except Exception as err:
            raise MappingError from err

    def dump(self, data: Any) -> Any:
        try:
            return self._retort.dump(data)
        except Exception as err:
            raise MappingError from err
