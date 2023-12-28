from decimal import Decimal
from typing import Any

from adaptix import name_mapping, Retort, loader, P

from cryptoapi.api.entities import Instrument, Candle, Quotes, CurrencyIndexPrice, Equity, Position
from cryptoapi.tools.mapper import Mapper


def _decimal_converter(raw: int | str | float) -> Decimal:
    return Decimal(str(raw))


_DERIBIT_RETORT = Retort(
    recipe=[
        name_mapping(Instrument, map=[{
            "section": "section",
            "title": ("model", "instrument_name"),
            "expire_period": ("model", "settlement_period"),
            "underlying_currency": ("model", "base_currency"),
            "margin_currency": ("model", "settlement_currency"),
            "quoted_currency": ("model", "quote_currency"),
            "commission_percent": ("model", "taker_commission"),
            "active_status": ("model", "is_active"),
        }, (".*", ("model", ...))]),
        loader(P[Instrument].commission_percent, lambda x: Decimal(str(x * 100))),
        loader(P[Instrument].min_trade_amount, _decimal_converter),
        loader(P[Instrument].contract_size, _decimal_converter),
        name_mapping(Quotes, map={"markup_price": "mark_price"}),
        loader(P[Quotes].index_price, _decimal_converter),
        loader(P[Quotes].markup_price, _decimal_converter),
        loader(P[CurrencyIndexPrice].index_price, _decimal_converter),
        name_mapping(Equity, map={"size": "equity"}),
        loader(P[Equity].size, _decimal_converter),
    ]
)

_DERIBIT_MAPPER = Mapper(_DERIBIT_RETORT)


def _candle_converter(raw: dict[str, list[str | float | int]]) -> list[Candle]:
    candles = []
    for ts, o, h, l, c in zip(raw["ticks"], raw["open"], raw["high"], raw["low"], raw["close"]):
        candles.append(Candle(int(ts), Decimal(str(o)), Decimal(str(h)), Decimal(str(l)), Decimal(str(c))))
    return candles


def _position_converter(raw: dict[str, Any], instrument: Instrument) -> Position:
    if instrument.is_direct:
        return Position(size=Decimal(str(raw["size_currency"])))
    return Position(size=Decimal(str(raw["size"])))
