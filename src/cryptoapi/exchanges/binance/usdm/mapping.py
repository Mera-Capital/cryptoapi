from decimal import Decimal
from typing import Union

from adaptix import Retort, name_mapping, loader

from cryptoapi.api.entities import Candle
from cryptoapi.tools.mapper import Mapper


def _decimal_converter(value: Union[str, int]) -> Decimal:
    return Decimal(value)


_BINANCE_UM_RETORT = Retort(
    recipe=[
        name_mapping(Candle, map={"timestamp": "T", "open": "o", "high": "h", "low": "l", "close": "c"}),
        loader(Decimal, _decimal_converter),
    ]
)

_BINANCE_UM_MAPPER = Mapper(_BINANCE_UM_RETORT)
