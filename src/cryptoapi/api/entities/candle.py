from dataclasses import dataclass
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cryptoapi.api.entities import Timeframe, Instrument


@dataclass(slots=True, frozen=True)
class Candle:
    timestamp: int
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal


@dataclass
class ClosedTimeframeEvent:
    timeframe: "Timeframe"
    instrument_title: "Instrument"
    candle: Candle
