from decimal import Decimal

from adaptix import Retort, name_mapping, loader, P

from cryptoapi.api.entities import Instrument
from cryptoapi.tools.mapper import Mapper

_SPOT_RETORT = Retort(
    recipe=[
        name_mapping(Instrument, map=[{
            "section": "section",
            "kind": "kind",
            "active_status": "active_status",
            "margin_currency": "margin_currency",
            "title": ("model", "symbol"),
            "underlying_currency": ("model", "baseAsset"),
            "quoted_currency": ("model", "quoteAsset"),
        }, (".*", ("model", ...))]),
    ]
)

_SPOT_MAPPER = Mapper(_SPOT_RETORT)
