from dataclasses import dataclass, field
from typing import Dict, Optional, Any


@dataclass
class RequestModel:
    method: str
    url: str
    headers: Dict[str, str] = field(default_factory=dict)
    params: Dict[str, str] = field(default_factory=dict)
    body: Optional[Any] = None
    auth: Optional[Dict[str, str]] = None

    def to_dict(self) -> dict:
        return {
            "method": self.method,
            "url": self.url,
            "headers": self.headers,
            "params": self.params,
            "body": self.body,
            "auth": self.auth,
        }

    @staticmethod
    def from_dict(data: dict) -> "RequestModel":
        return RequestModel(
            method=data.get("method", "GET"),
            url=data.get("url", ""),
            headers=data.get("headers", {}),
            params=data.get("params", {}),
            body=data.get("body"),
            auth=data.get("auth"),
        )