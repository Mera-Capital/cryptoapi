import pytest

from cryptoapi.exchanges.deribit import Deribit
from cryptoapi.exchanges.deribit.access import AccessToken
from cryptoapi.tools.timestamp import ms_utc

SCOPE = ("block_trade:read_write "
         "trade:read_write "
         "wallet:read_write "
         "account:read_write "
         "custody:read_write "
         "session:rest-64N+Ik5BE5M= "
         "mainaccount")
BAD_SCOPE = ("block_trade:read_write "
             "trade:read "
             "wallet:read "
             "account:read "
             "custody:read "
             "session:rest-64N+Ik5BE5M= "
             "mainaccount")
BAD_SCOPE_PARTIAL = ("block_trade:read_write "
                     "wallet:read "
                     "account:read "
                     "custody:read "
                     "session:rest-64N+Ik5BE5M= "
                     "mainaccount")
ACCESS_TOKEN = AccessToken("access_token", "refresh_token", 1000, ms_utc(), SCOPE)


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
    deribit._tokens_store["client_idclient_secret"] = ACCESS_TOKEN
    # Act
    headers = await deribit._get_headers(creds)
    # Assert
    assert headers == expected


async def test_not_expire_auth(deribit: Deribit) -> None:
    # Arrange
    expected = {"Authorization": "Bearer access_token", "Content-Type": "application/json"}
    creds = {"client_id": "client_id", "client_secret": "client_secret"}
    deribit._tokens_store["client_idclient_secret"] = ACCESS_TOKEN
    # Act
    headers = await deribit._get_headers(creds)
    # Assert
    assert headers == expected


@pytest.mark.parametrize("token, expected", [
    (AccessToken("access_token", "refresh_token", 1000, ms_utc(), SCOPE), True),
    (AccessToken("access_token", "refresh_token", 1000, ms_utc(), BAD_SCOPE), False),
    (AccessToken("access_token", "refresh_token", 1000, ms_utc(), BAD_SCOPE_PARTIAL), False),
])
def test_check_scope(token: AccessToken, expected: bool) -> None:
    assert token.scope_is_valid == expected
