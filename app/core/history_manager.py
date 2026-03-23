import json
import os
from typing import List

from app.models.request_model import RequestModel


class HistoryManager:
    def __init__(self, file_path="data/history.json"):
        self.file_path = file_path
        self.history: List[RequestModel] = []
        self._load()

    def add(self, request: RequestModel):
        self.history.insert(0, request)  # najnowsze na górze
        self._save()

    def get_all(self) -> List[RequestModel]:
        return self.history

    def _load(self):
        if not os.path.exists(self.file_path):
            self._create_empty_file()

        with open(self.file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                self.history = [RequestModel.from_dict(item) for item in data]
            except json.JSONDecodeError:
                self.history = []

    def _save(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([req.to_dict() for req in self.history], f, indent=2)

    def _create_empty_file(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)