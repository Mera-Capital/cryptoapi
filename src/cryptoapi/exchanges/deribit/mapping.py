from decimal import Decimal

from adaptix import name_mapping, Retort, loader, P

from cryptoapi.api.entities import Instrument, Candle, Quotes
from cryptoapi.tools.mapper import Mapper

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
        loader(P[Instrument].min_trade_amount, lambda x: Decimal(str(x))),
        loader(P[Instrument].contract_size, lambda x: Decimal(str(x))),
        name_mapping(Quotes, map={"markup_price": "mark_price"}),
        loader(P[Quotes].index_price, lambda x: Decimal(str(x))),
        loader(P[Quotes].markup_price, lambda x: Decimal(str(x))),
    ]
)

_DERIBIT_MAPPER = Mapper(_DERIBIT_RETORT)


def _candle_converter(raw: dict[str, list[str | float | int]]) -> list[Candle]:
    candles = []
    for ts, o, h, l, c in zip(raw["ticks"], raw["open"], raw["high"], raw["low"], raw["close"]):
        candles.append(Candle(int(ts), Decimal(str(o)), Decimal(str(h)), Decimal(str(l)), Decimal(str(c))))
    return candles
