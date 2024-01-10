from typing import Any

from cryptoapi.api import entities
from cryptoapi.clients.wss import BaseWSSClient
from cryptoapi.exchanges.binance.usdm.mapping import _BINANCE_UM_MAPPER
from cryptoapi.exchanges.binance.usdm.url import WSSBinanceUMURL


class WSSBinanceUMClient(BaseWSSClient):
    def __init__(self, testnet: bool) -> None:
        self._url = WSSBinanceUMURL(testnet)
        super().__init__(uri=self._url.base)
        self.mapper = _BINANCE_UM_MAPPER

    @staticmethod
    def create_message_for_chart_data(instrument_name: str, timeframe: int) -> dict[str, Any]:
        channel = [f"{instrument_name.lower()}@kline_{timeframe}m"]
        return {"method": "SUBSCRIBE", "params": channel, "id": 1}

    async def listen(self) -> entities.ClosedTimeframeEvent | None:
        response = await self.listen_socket()
        if response.get("k"):
            return self._pars_response_for_chart_data(response["k"])
        return None

    def _pars_response_for_chart_data(self, response: dict[str, Any]) -> entities.ClosedTimeframeEvent:
        instrument_name = response.get("s")
        timeframe = response.get("i")
        candle = self.mapper.load(response, entities.Candle)
        return entities.ClosedTimeframeEvent(
            timeframe=entities.Timeframe(int(timeframe[0])),  # type:ignore[index]
            instrument_title=instrument_name,  # type:ignore[arg-type]
            candle=candle,
        )

# async def main():
#     async with WSSBinanceUMClient(True) as cli:
#         message = cli.create_message_for_chart_data('BTCUSDT', 1)
#         print(message)
#         await cli.subscribe(message)
#         while cli.socket.open:
#             print(await cli.listen())
#
#
# asyncio.run(main())
