from dataclasses import dataclass

from cryptoapi.exchanges.deribit.constants import SCOPE_PERMISSIONS
from cryptoapi.tools.timestamp import ms_utc


@dataclass
class AccessToken:
    access_token: str
    refresh_token: str
    expire_delta: int
    creation_timestamp: int
    scope: str

    @classmethod
    def create(cls, raw_tokens: dict[str, int | str]) -> "AccessToken":
        return cls(
            access_token=raw_tokens["access_token"],  # type: ignore[arg-type]
            refresh_token=raw_tokens["refresh_token"],  # type: ignore[arg-type]
            expire_delta=int(raw_tokens["expires_in"]) * 1000,  # to milliseconds
            creation_timestamp=ms_utc(),
            scope=raw_tokens["scope"],  # type: ignore[arg-type]
        )

    @property
    def is_expire(self) -> bool:
        timestamp_now = ms_utc()
        expire_difference = 5000  # milliseconds
        if timestamp_now >= self.creation_timestamp + self.expire_delta - expire_difference:
            return True
        return False

    @property
    def scope_is_valid(self) -> bool:
        permissions = {perm.split(":")[0]: perm.split(":")[1] for perm in self.scope.split(" ")[:-1]}
        for key, value in SCOPE_PERMISSIONS.items():
            perm = permissions.get(key, None)
            if perm and perm not in value:
                return False
            if not perm:
                return False
        return True
