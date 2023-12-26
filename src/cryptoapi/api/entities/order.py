from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class OrderType(str, Enum):
    SPOT = "spot"
    LIMIT = "limit"


class OrderDirection(str, Enum):
    BUY = "buy"
    SELL = "sell"


class OrderState(str, Enum):
    FILLED = "filled"
    UNFULFILLED = "unfulfilled"


@dataclass(slots=True, frozen=True)
class OrderInfo:
    instrument_title: str
    average_price: Decimal
    original_amount: Decimal
    executed_amount: Decimal
    state: OrderState
    direction: OrderDirection
    type: OrderType
