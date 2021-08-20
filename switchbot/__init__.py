from typing import List
from switchbot.devices import Device

from switchbot.client import SwitchBotClient


class SwitchBot:
    def __init__(self, token: str):
        self.client = SwitchBotClient(token)

    def devices(self) -> List[Device]:
        response = self.client.get('devices')
        return [self.device(device['device_id'], **device)
                for device in response['body']['device_list']]

    def device(self, id: str, **extra) -> Device:
        return Device(client=self.client, id=id, **extra)
