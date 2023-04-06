from __future__ import annotations

from switchbot.client import SwitchBotClient


class Scene:
    def __init__(self, client: SwitchBotClient, id: str, **extra):
        self.client = client
        self.id: str = id
        self.name: str = extra.get("scene_name")

    def execute(self):
        self.client.post(f"scenes/{self.id}/execute")

    def __repr__(self):
        name = "Scene" if self.name is None else self.name
        name = name.replace(" ", "")
        return f"{name}(id={self.id})"
