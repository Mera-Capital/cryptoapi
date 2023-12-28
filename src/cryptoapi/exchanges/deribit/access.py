from dataclasses import dataclass

from cryptoapi.tools.timestamp import ms_utc


@dataclass
class AccessToken:
    access_token: str
    refresh_token: str
    expire_delta: int
    creation_timestamp: int

    @property
    def is_expire(self) -> bool:
        timestamp_now = ms_utc()
        expire_difference = 5000  # milliseconds
        if timestamp_now >= self.creation_timestamp + self.expire_delta - expire_difference:
            return True
        return False

    @classmethod
    def create(cls, raw_tokens: dict[str, int | str]) -> "AccessToken":
        return cls(
            access_token=raw_tokens["access_token"],  # type: ignore[arg-type]
            refresh_token=raw_tokens["refresh_token"],  # type: ignore[arg-type]
            expire_delta=int(raw_tokens["expires_in"]) * 1000,  # to milliseconds
            creation_timestamp=ms_utc(),
        )
