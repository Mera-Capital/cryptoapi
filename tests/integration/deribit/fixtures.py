from decimal import Decimal

from cryptoapi.api.entities import Instrument, Section, Kind

BTC_PERPETUAL_CORRECT = Instrument(
    title="BTC-PERPETUAL",
    section=Section.MAIN,
    expire_period="perpetual",
    underlying_currency="BTC",
    margin_currency="BTC",
    quoted_currency="USD",
    contract_size=Decimal("0.01"),
    commission_percent=Decimal("0.05"),
    min_trade_amount=Decimal("0.01"),
    kind=Kind.FUTURE,
    active_status=True,
    creation_timestamp=1502245256000,
)

BTC_PERPETUAL_IS_DIRECT = Instrument(
    title="BTC-PERPETUAL",
    section=Section.MAIN,
    expire_period="perpetual",
    underlying_currency="BTC",
    margin_currency="USD",
    quoted_currency="USD",
    contract_size=Decimal("0.01"),
    commission_percent=Decimal("0.05"),
    min_trade_amount=Decimal("0.01"),
    kind=Kind.FUTURE,
    active_status=True,
    creation_timestamp=1502245256000,
)
