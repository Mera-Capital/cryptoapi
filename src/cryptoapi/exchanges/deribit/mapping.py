from decimal import Decimal

from adaptix import name_mapping, Retort, loader, P

from cryptoapi.api.entities import Instrument
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
    ]
)

_DERIBIT_MAPPER = Mapper(_DERIBIT_RETORT)
