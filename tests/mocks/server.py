import json
from pathlib import Path
from typing import Any

from aioresponses import aioresponses


class MockServer(aioresponses):
    def __init__(self, responses_path: Path) -> None:
        super().__init__()
        self.path = responses_path

    def save(self, exchange: str, url: str, payload: dict[Any, Any]) -> None:
        with open(self._generate_path(exchange, url), "a") as file:
            json.dump(payload, file)

    def load(self, exchange: str, url: str) -> dict[Any, Any]:
        with open(self._generate_path(exchange, url), "r") as file:
            data = json.loads(file.read())
        return data

    def _generate_path(self, exchange: str, url: str) -> Path:
        return self.path / exchange / f"{url}.json"
