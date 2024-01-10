from typing import Any


class MockListenCoro:
    @staticmethod
    async def is_response(self) -> dict[str, Any]:
        return {
            "e": "kline",
            "E": 1704886287364,
            "s": "BTCUSD_PERP",
            "k": {
                "t": 1704886260000,
                "T": 1704886319999,
                "s": "BTCUSD_PERP",
                "i": "1m",
                "f": 98059883,
                "L": 98059884,
                "o": "45601.3",
                "c": "49799.9",
                "h": "49799.9",
                "l": "45601.3",
                "v": "2",
                "n": 2,
                "x": False,
                "q": "0.00420096",
                "V": "1",
                "Q": "0.00200804",
                "B": "0"
            }
        }

    @staticmethod
    async def is_not_response(self) -> dict[str, Any]:
        return {"result": None, "id": 1}
