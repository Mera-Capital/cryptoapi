from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class Kind(str, Enum):
    FUTURE = "future"
    SPOT = "spot"


class Section(str, Enum):
    USDM = "usdm"
    COINM = "coinm"
    SPOT = "spot"
    MAIN = "main"


class Timeframe(int, Enum):
    M1 = 1
    M5 = 5
    M15 = 15
    M30 = 30


@dataclass(slots=True, frozen=True)
class Instrument:
    title: str
    section: Section
    underlying_currency: str
    margin_currency: str
    quoted_currency: str
    kind: Kind
    active_status: bool
    creation_timestamp: int | None = None
    min_trade_amount: Decimal | None = None
    contract_size: Decimal | None = None

    @property
    def is_direct(self) -> bool:
        if self.underlying_currency.lower() != self.margin_currency.lower():
            return True
        return False
