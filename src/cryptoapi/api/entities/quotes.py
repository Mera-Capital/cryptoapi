from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True, frozen=True)
class Quotes:
    index_price: Decimal
    markup_price: Decimal
    timestamp: int
