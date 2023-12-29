from typing import Any

from cryptoapi.api import entities
from cryptoapi.clients.wss import BaseWSSClient
from cryptoapi.exchanges.deribit.mapping import _DERIBIT_MAPPER


class WSSDeribitClient(BaseWSSClient):
    def __init__(self, uri: str):
        super().__init__(uri=uri)
        self.mapper = _DERIBIT_MAPPER

    async def listen(self) -> entities.ClosedTimeframeEvent | None:
        response = await self.listen_socket()
        if not response.get("result"):
            return self._pars_response_for_chart_data(response)
        return None

    @staticmethod
    def create_message_for_chart_data(instrument_name: str, timeframe: int) -> dict[str, Any]:
        channel = [f'chart.trades.{instrument_name}.{timeframe}']
        return {
            "jsonrpc": "2.0",
            "method": "public/subscribe",
            "params": {
                "channels": channel
            }
        }

    def _pars_response_for_chart_data(self, response: dict[str, Any]) -> entities.ClosedTimeframeEvent:
        params = response["params"]
        _, _, instrument_name, timeframe = params["channel"].split(".")
        candle = self.mapper.load(params["data"], entities.Candle)
        return entities.ClosedTimeframeEvent(
            timeframe=entities.Timeframe(int(timeframe)),
            instrument_title=instrument_name,
            candle=candle,
        )

# async def main():
#     async for client in WSSDeribitClient('wss://test.deribit.com/den/ws'):
#         try:
#             message = client.create_message_for_chart_data('BTC-PERPETUAL', 1)
#             await client.subscribe(message)
#             while client.socket.open:
#                 print(await client.listen())
#         except (ConnectionClosed, gaierror):
#             continue
#
#
# asyncio.get_event_loop().run_until_complete(main())
