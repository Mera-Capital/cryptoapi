from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True, frozen=True)
class OperationsSummary:
    withdrawal_sum: Decimal
    deposit_sum: Decimal
