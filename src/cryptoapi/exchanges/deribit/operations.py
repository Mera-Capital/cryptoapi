from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Operation:
    amount: Decimal
    currency: str
    state: str
    updated_timestamp: int


@dataclass
class Transfer(Operation):
    direction: str
