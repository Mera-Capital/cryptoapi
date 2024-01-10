from dataclasses import dataclass

from .base import APIException


@dataclass(eq=False)
class TimeoutAPIError(APIException):
    pass


@dataclass(eq=False)
class BadResponseAPIError(APIException):
    message: str = "default message"
    error_code: int = 0
