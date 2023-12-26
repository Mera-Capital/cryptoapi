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
    expire_period: str
    underlying_currency: str
    margin_currency: str
    quoted_currency: str
    contract_size: int
    commission_percent: Decimal
    min_trade_amount: Decimal
    kind: Kind
    active_status: bool
    creation_timestamp: int
