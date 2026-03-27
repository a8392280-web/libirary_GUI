from dataclasses import dataclass
from typing import Any


@dataclass
class ApiResponse:
    ok: bool
    status_code: int
    data: Any = None
    error: str = None