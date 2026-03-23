from dataclasses import dataclass, field
from typing import List, Dict

from app.models.collection_model import CollectionModel
from app.models.request_model import RequestModel


@dataclass
class ProjectModel:
    collections: List[CollectionModel] = field(default_factory=list)
    history: List[RequestModel] = field(default_factory=list)
    environments: Dict[str, str] = field(default_factory=dict)

    def to_dict(self):
        return {
            "collections": [c.to_dict() for c in self.collections],
            "history": [h.to_dict() for h in self.history],
            "environments": self.environments
        }

    @staticmethod
    def from_dict(data: dict) -> "ProjectModel":
        return ProjectModel(
            collections=[
                CollectionModel.from_dict(c)
                for c in data.get("collections", [])
            ],
            history=[
                RequestModel.from_dict(h)
                for h in data.get("history", [])
            ],
            environments=data.get("environments", {})
        )