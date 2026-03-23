import json
import os
from typing import List

from app.models.collection_model import CollectionModel
from app.models.request_model import RequestModel


class CollectionManager:
    def __init__(self, file_path="data/collections.json"):
        self.file_path = file_path
        self.collections: List[CollectionModel] = []
        self._load()

    def create_collection(self, name: str):
        self.collections.append(CollectionModel(name=name))
        self._save()

    def add_request(self, collection_name: str, request: RequestModel):
        for col in self.collections:
            if col.name == collection_name:
                col.requests.append(request)
                self._save()
                return

    def get_all(self) -> List[CollectionModel]:
        return self.collections

    def _load(self):
        if not os.path.exists(self.file_path):
            self._create_empty_file()

        with open(self.file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                self.collections = [
                    CollectionModel.from_dict(c) for c in data
                ]
            except json.JSONDecodeError:
                self.collections = []

    def _save(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([c.to_dict() for c in self.collections], f, indent=2)

    def _create_empty_file(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)