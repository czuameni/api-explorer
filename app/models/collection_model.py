from dataclasses import dataclass, field
from typing import List

from app.models.request_model import RequestModel


@dataclass
class CollectionModel:
    name: str
    requests: List[RequestModel] = field(default_factory=list)

    def to_dict(self):
        return {
            "name": self.name,
            "requests": [req.to_dict() for req in self.requests]
        }

    @staticmethod
    def from_dict(data: dict) -> "CollectionModel":
        return CollectionModel(
            name=data.get("name", "Unnamed"),
            requests=[
                RequestModel.from_dict(r) for r in data.get("requests", [])
            ]
        )