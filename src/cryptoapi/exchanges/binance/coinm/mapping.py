from decimal import Decimal

from adaptix import Retort, name_mapping, loader, P

from cryptoapi.api.entities import Instrument
from cryptoapi.tools.mapper import Mapper

_COINM_RETORT = Retort(
    recipe=[
        name_mapping(Instrument, map=[{
            "section": "section",
            "kind": "kind",
            "active_status": "active_status",
            "min_trade_amount": "min_trade_amount",
            "title": ("model", "symbol"),
            "underlying_currency": ("model", "baseAsset"),
            "margin_currency": ("model", "marginAsset"),
            "quoted_currency": ("model", "quoteAsset"),
            "contract_size": ("model", "contractSize"),
            "creation_timestamp": ("model", "onboardDate")
        }, (".*", ("model", ...))]),
        loader(P[Instrument].contract_size, lambda x: Decimal(str(x))),
    ]
)

_COINM_MAPPER = Mapper(_COINM_RETORT)
