from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True, frozen=True)
class Equity:
    size: Decimal
