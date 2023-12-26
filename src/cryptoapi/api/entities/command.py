from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class CommandStatus:
    success: bool
    payload: dict[str, Any]
