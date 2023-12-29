from cryptoapi.api.entities import CommandStatus
from cryptoapi.exchanges.deribit import Deribit
from tests.mocks import MockServer


async def test_credentials_scope(deribit: Deribit, server_mock: MockServer) -> None:
    # Arrange
    expected = CommandStatus(success=False, payload={"message": "invalid scope"})
    server_mock.clear()  # Clear valid scope response
    creds = {"client_id": "client_id", "client_secret": "client_secret"}
    url = ("https://test.deribit.com/api/v2/public/auth?"
           "client_id=client_id&client_secret=client_secret&grant_type=client_credentials")
    server_mock.get(url, payload=server_mock.load("deribit", "check_creds_invalid_scope"))
    # Act
    result = await deribit.check_credentials(creds)
    server_mock.clear()  # Clear invalid scope response
    # Assert
    assert expected == result


async def test_credentials_auth(deribit: Deribit, server_mock: MockServer) -> None:
    # Arrange
    expected = CommandStatus(success=False, payload={"message": "invalid_credentials"})
    server_mock.clear()  # Clear valid auth response
    creds = {"client_id": "client_id", "client_secret": "client_secret"}
    url = ("https://test.deribit.com/api/v2/public/auth?"
           "client_id=client_id&client_secret=client_secret&grant_type=client_credentials")
    server_mock.get(url, payload=server_mock.load("deribit", "check_creds_invalid_api_keys"), status=403)
    # Act
    result = await deribit.check_credentials(creds)
    server_mock.clear()  # Clear invalid auth response
    # Assert
    assert expected == result
