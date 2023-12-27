import pytest
from aioresponses import aioresponses


@pytest.fixture(autouse=True)
def server_mock() -> "aioresponses":
    with aioresponses() as server:
        yield server
