from typing import Any, Dict, List, Optional

import humps

from switchbot.client import SwitchBotClient


class Device:
    def __init__(self, client: SwitchBotClient, id: str, **extra):
        self.client = client

        self.id: str = id
        self.name: str = extra.get('device_name')
        self.type: bool = extra.get('device_type')
        self.cloud_enabled: bool = extra.get('enable_cloud_service')
        self.hub_id: str = extra.get('hub_device_id')

        self.curtain_ids: List[str] = extra.get('curtain_devices_ids')
        self.calibrated: bool = extra.get('calibrate')
        self.grouped: bool = extra.get('group')
        self.master: bool = extra.get('master')
        self.open_direction: str = extra.get('open_direction')

    def status(self) -> Dict[str, Any]:
        mapping = {'power': 'power',
                   'humidity': 'humidity',
                   'temperature': 'temperature',
                   'nebulization_efficiency': 'nebulization_efficiency',
                   'auto': 'auto',
                   'child_lock': 'safety_lock',
                   'sound': 'sound',
                   'calibrate': 'calibrate',
                   'group': 'grouped',
                   'moving': 'moving',
                   'slide_position': 'slide_position',
                   'mode': 'mode',
                   'speed': 'speed',
                   'speed': 'speed',
                   'shaking': 'oscillating',
                   'shake_center': 'oscillating_center',
                   'shake_range': 'oscillating_range'}

        response = self.client.get(f'devices/{self.id}/status')
        return {mapping[key]: value
                for key, value in response['body'].items()
                if key in mapping}

    def command(self, action: str, parameter: Optional[str] = None):
        parameter = 'default' if parameter is None else parameter
        payload = humps.camelize({
            'command_type': 'command',
            'command': humps.camelize(action),
            'parameter': parameter})

        self.client.post(f'devices/{self.id}/commands', json=payload)


    def __repr__(self):
        name = 'Device' if self.type is None else self.type
        name = name.replace(' ', '')
        return f'{name}(id={self.id})'