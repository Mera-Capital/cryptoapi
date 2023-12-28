import asyncio
import json
from decimal import Decimal
from typing import Any

from adaptix import Retort, name_mapping, loader

from cryptoapi.api import entities
from cryptoapi.clients.wss import BaseWSSClient

RETORT = Retort(
    recipe=[
        name_mapping(entities.Candle, map={"timestamp": "tick"}),
        loader(Decimal, lambda x: Decimal(x)),
    ]
)


class WSSDeribitClient(BaseWSSClient):
    def __init__(self, uri: str):
        super().__init__(uri=uri)
        self.mapper = RETORT

    async def listen_socket(self) -> entities.ClosedTimeframeEvent:
        response = json.loads(await self.socket.recv())
        if not response.get("result"):
            return self._pars_response_for_chart_data(response)

    @staticmethod
    def create_message_for_chart_data(instrument_name, timeframe: int) -> dict[str, Any]:
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


async def main():
    async with WSSDeribitClient('wss://test.deribit.com/den/ws') as client:
        message = client.create_message_for_chart_data('BTC-PERPETUAL', 1)
        await client.subscribe(message)
        while client.socket.open:
            print(await client.listen_socket())


asyncio.get_event_loop().run_until_complete(main())
