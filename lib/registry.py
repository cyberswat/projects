import json
import os
from pathlib import Path
from datetime import datetime

class Registry:
    def __init__(self, path="~/.claude/projects.json"):
        self.path = Path(path).expanduser()

    def load(self):
        if self.path.exists():
            return json.loads(self.path.read_text())
        return {"projects": {}}

    def save(self, data):
        self.path.parent.mkdir(exist_ok=True)
        self.path.write_text(json.dumps(data, indent=2))

    def add(self, name, path):
        data = self.load()
        data["projects"][name] = {
            "path": str(Path(path).expanduser()),
            "last_worked": datetime.now().strftime("%Y-%m-%d")
        }
        self.save(data)

    def remove(self, name):
        data = self.load()
        data["projects"].pop(name, None)
        self.save(data)

    def list(self):
        data = self.load()
        return data["projects"]

    def worked(self, name):
        data = self.load()
        if name in data["projects"]:
            data["projects"][name]["last_worked"] = datetime.now().strftime("%Y-%m-%d")
            self.save(data)
