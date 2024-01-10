from decimal import Decimal

from cryptoapi.api.entities import OperationsSummary
from cryptoapi.exchanges.deribit import Deribit
from tests.integration.deribit.fixtures import BTC_PERPETUAL_CORRECT
from tests.mocks import MockServer


async def test_operation_summary(deribit: Deribit, server_mock: MockServer) -> None:
    # Arrange
    expected = OperationsSummary(withdrawal_sum=Decimal("64.0"), deposit_sum=Decimal("0"))
    creds = {"client_id": "client_id", "client_secret": "client_secret"}
    withdrawals = deribit._url.withdrawals.format(currency=BTC_PERPETUAL_CORRECT.margin_currency)
    transfers = deribit._url.transfers.format(currency=BTC_PERPETUAL_CORRECT.margin_currency)
    deposits = deribit._url.deposits.format(currency=BTC_PERPETUAL_CORRECT.margin_currency)
    server_mock.get(withdrawals, payload=server_mock.load("deribit", "withdrawals_btc"))
    server_mock.get(transfers, payload=server_mock.load("deribit", "transfers_btc"))
    server_mock.get(deposits, payload=server_mock.load("deribit", "deposits_btc"))
    # Act
    summary = await deribit.get_operations_summary(BTC_PERPETUAL_CORRECT, 1666894490480, 1686894490480, creds)
    # Assert
    assert expected == summary
