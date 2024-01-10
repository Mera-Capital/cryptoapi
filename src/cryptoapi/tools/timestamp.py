from datetime import datetime, timezone


def ms_utc() -> int:
    return int(datetime.now(tz=timezone.utc).timestamp() * 1000)
