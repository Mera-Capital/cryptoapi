from cryptoapi.exchanges.deribit import Deribit
from cryptoapi.exchanges.deribit.access import AccessToken
from cryptoapi.tools.timestamp import ms_utc


async def test_auth(deribit: Deribit) -> None:
    # Arrange
    expected = {"Authorization": "Bearer access_token", "Content-Type": "application/json"}
    creds = {"client_id": "client_id", "client_secret": "client_secret"}
    # Act
    headers = await deribit._get_headers(creds)
    # Assert
    assert headers == expected


async def test_expire_auth(deribit: Deribit) -> None:
    # Arrange
    expected = {"Authorization": "Bearer access_token", "Content-Type": "application/json"}
    creds = {"client_id": "client_id", "client_secret": "client_secret"}
    deribit._tokens_store["client_idclient_secret"] = AccessToken("access_token", "refresh_token", 1000, ms_utc())
    # Act
    headers = await deribit._get_headers(creds)
    # Assert
    assert headers == expected


async def test_not_expire_auth(deribit: Deribit) -> None:
    # Arrange
    expected = {"Authorization": "Bearer access_token", "Content-Type": "application/json"}
    creds = {"client_id": "client_id", "client_secret": "client_secret"}
    deribit._tokens_store["client_idclient_secret"] = AccessToken("access_token", "refresh_token", 10000, ms_utc())
    # Act
    headers = await deribit._get_headers(creds)
    # Assert
    assert headers == expected
