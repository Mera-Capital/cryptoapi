from decimal import Decimal

SCOPE_PERMISSIONS = {
    "account": ["read_write", "read"],
    "block_trade": ["read_write", "read"],
    "trade": ["read_write"],
    "wallet": ["read_write", "read"],
}
INVALID_CREDS_CODE = 13004
CONTRACT_VALUE_ROUNDING = {"BTC": Decimal("1.000"), "ETH": Decimal("1.00")}
