import json
import os

from app.models.project_model import ProjectModel


class ProjectManager:

    @staticmethod
    def save(project: ProjectModel, file_path: str):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(project.to_dict(), f, indent=2)

    @staticmethod
    def load(file_path: str) -> ProjectModel:
        if not os.path.exists(file_path):
            return ProjectModel()

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return ProjectModel.from_dict(data)