from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ResponseModel:
    status_code: int
    headers: Dict[str, str]
    body: Any
    response_time: float
    size: int

    def is_success(self) -> bool:
        return 200 <= self.status_code < 300