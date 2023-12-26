from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True, frozen=True)
class Candle:
    timestamps: int
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
