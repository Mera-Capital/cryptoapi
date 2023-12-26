from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True, frozen=True)
class CurrencyIndexPrice:
    index_price: Decimal
    timestamp: int
