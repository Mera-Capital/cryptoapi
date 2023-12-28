from dataclasses import dataclass
from decimal import Decimal

from cryptoapi.api import entities


@dataclass(slots=True, frozen=True)
class Candle:
    timestamp: int
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal


@dataclass
class ClosedTimeframeEvent:
    timeframe: entities.Timeframe
    instrument_title: entities.Instrument
    candle: Candle
