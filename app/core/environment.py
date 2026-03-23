import re


class EnvironmentManager:
    def __init__(self):
        self.variables = {}

    def set(self, key: str, value: str):
        self.variables[key] = value

    def get(self, key: str):
        return self.variables.get(key)

    def load(self, data: dict):
        self.variables = data or {}

    def to_dict(self):
        return self.variables

    def resolve(self, text: str) -> str:
        if not text:
            return text

        pattern = r"\{\{(.*?)\}\}"

        def replace(match):
            key = match.group(1).strip()
            return self.variables.get(key, match.group(0))

        return re.sub(pattern, replace, text)