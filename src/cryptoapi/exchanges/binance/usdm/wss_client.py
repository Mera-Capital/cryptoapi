from typing import Any

from cryptoapi.api import entities
from cryptoapi.clients.wss import BaseWSSClient
from cryptoapi.exchanges.binance.usdm.mapping import _BINANCE_UM_MAPPER


class WSSBinanceUMClient(BaseWSSClient):
    def __init__(self, uri: str):
        super().__init__(uri=uri)
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
#     async with WSSBinanceUMClient('wss://fstream.binance.com/ws') as client:
#         message = client.create_message_for_chart_data('btcusdt', 1)
#         await client.subscribe(message)
#         while client.socket.open:
#             print(await client.listen())
#
#
# asyncio.get_event_loop().run_until_complete(main())
