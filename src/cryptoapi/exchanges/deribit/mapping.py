from decimal import Decimal
from typing import Any

from adaptix import name_mapping, Retort, loader, P

from cryptoapi.api.entities import (
    Instrument,
    Candle,
    Quotes,
    CurrencyIndexPrice,
    Equity,
    Position,
    OrderInfo,
    OperationsSummary,
)
from cryptoapi.exchanges.deribit.operations import Operation, Transfer
from cryptoapi.tools.mapper import Mapper
from cryptoapi.tools.timestamp import ms_utc


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
        name_mapping(OrderInfo, map={
            "state": "order_state",
            "instrument_title": "instrument_name",
            "original_amount": "amount",
            "executed_amount": "filled_amount",
            "type": "order_type",
        }),
        loader(P[OrderInfo].executed_amount, _decimal_converter),
        loader(P[OrderInfo].average_price, _decimal_converter),
        loader(P[OrderInfo].original_amount, _decimal_converter),
        loader(P[Operation].amount, _decimal_converter),
        loader(P[Transfer].amount, _decimal_converter),
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


def _operations_summary_converter(
        withs: list[Operation],
        trans: list[Transfer],
        deps: list[Operation],
        date_from: int,
) -> OperationsSummary:
    date_to = ms_utc()
    if trans:
        sum_trans_out = Decimal(sum(list(t.amount for t in trans if t.state == "confirmed" and t.direction == "payment"
                                         and date_from < t.updated_timestamp < date_to)))
        sum_trans_in = Decimal(sum(list(t.amount for t in trans if t.state == "confirmed" and t.direction == "income"
                                        and date_from < t.updated_timestamp < date_to)))
    else:
        sum_trans_in, sum_trans_out = Decimal(), Decimal()

    if withs:
        sum_withs = Decimal(sum(list(w.amount for w in withs if w.state == "confirmed"
                                     and date_from < w.updated_timestamp < date_to)))
    else:
        sum_withs = Decimal()

    if deps:
        sum_deps = Decimal(sum(list(d.amount for d in deps if d.state == "completed"
                                    and date_from < d.updated_timestamp < date_to)))
    else:
        sum_deps = Decimal()

    return OperationsSummary(withdrawal_sum=sum_withs + sum_trans_out, deposit_sum=sum_deps + sum_trans_in)
