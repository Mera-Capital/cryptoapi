from adaptix import name_mapping, Retort

from cryptoapi.api.entities import Candle
from cryptoapi.tools.mapper import Mapper

_DERIBIT_RETORT = Retort(
    recipe=[
        name_mapping(Candle, map={'timestamps': 'ticks'}),
    ]
)

_DERIBIT_MAPPER = Mapper(_DERIBIT_RETORT)
