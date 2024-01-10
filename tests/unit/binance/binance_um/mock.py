from typing import Any


class MockListenCoro:
    @staticmethod
    async def is_response(self) -> dict[str, Any]:
        return {
            "e": "kline",
            "E": 1704885193041,
            "s": "BTCUSDT",
            "k": {
                "t": 1704885180000,
                "T": 1704885239999,
                "s": "BTCUSDT",
                "i": "1m",
                "f": 277882894,
                "L": 277882910,
                "o": "46481.20",
                "c": "46677.40",
                "h": "46749.00",
                "l": "46481.20",
                "v": "11.334",
                "n": 17,
                "x": None,
                "q": "527802.46540",
                "V": "4.770",
                "Q": "222699.86860",
                "B": "0"
            }
        }

    @staticmethod
    async def is_not_response(self) -> dict[str, Any]:
        return {"result": None, "id": 1}
