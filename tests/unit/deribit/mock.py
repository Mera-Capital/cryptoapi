from typing import Any


class MockListenCoro:
    @staticmethod
    async def is_response(self) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "method": "subscription",
            "params": {
                "channel": "chart.trades.BTC-PERPETUAL.1",
                "data": {
                    "volume": 0.23594088,
                    "tick": 1704882960000,
                    "open": 45657.0,
                    "low": 45642.5,
                    "high": 45657.0,
                    "cost": 10770.0,
                    "close": 45643.5
                }
            }
        }

    @staticmethod
    async def is_not_response(self) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "result": ["chart.trades.BTC-PERPETUAL.1"],
            "testnet": True,
            "usIn": 1704882989988722,
            "usOut": 1704882989988869,
            "usDiff": 147,
        }
