import pytest

from pathlib import Path

from tests.mocks import MockServer


@pytest.fixture(autouse=True)
def server_mock() -> MockServer:
    responses_path = Path(__file__).parent / "files"
    with MockServer(responses_path) as server:
        yield server
