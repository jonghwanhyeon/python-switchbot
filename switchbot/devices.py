from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Optional

import humps

from switchbot.client import SwitchBotClient

status_key_mapping = {
    'power': 'power',
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
    'shake_range': 'oscillating_range'
}


class Device:
    device_type_for: ClassVar[Optional[str]] = None
    specialized_cls: ClassVar[Dict[str, Device]] = {}

    def __init__(self, client: SwitchBotClient, id: str, **extra):
        self.client = client

        self.id: str = id
        self.name: str = extra.get('device_name')
        self.type: str = extra.get('device_type')
        self.cloud_enabled: bool = extra.get('enable_cloud_service')
        self.hub_id: str = extra.get('hub_device_id')

    def __init_subclass__(cls):
        if cls.device_type_for is not None:
            cls.specialized_cls[cls.device_type_for] = cls

    @classmethod
    def create(cls, client: SwitchBotClient, id: str, **extra):
        device_type = extra.get('device_type')
        device_cls = cls.specialized_cls.get(device_type, Device)
        return device_cls(client, id=id, **extra)

    def status(self) -> Dict[str, Any]:
        response = self.client.get(f'devices/{self.id}/status')
        return {status_key_mapping[key]: value
                for key, value in response['body'].items()
                if key in status_key_mapping}

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


class Bot(Device):
    device_type_for = 'Bot'

    def turn(self, state: str):
        state = state.lower()
        assert state in ('on', 'off')
        self.command(f'turn_{state}')

    def press(self):
        self.command('press')

    def toggle(self):
        state = self.status()['power']
        self.turn('on' if state == 'off' else 'off')


class Curtain(Device):
    device_type_for = 'Curtain'

    def __init__(self, client: SwitchBotClient, id: str, **extra):
        super().__init__(self, id, **extra)

        self.curtain_ids: List[str] = extra.get('curtain_devices_ids')
        self.calibrated: bool = extra.get('calibrate')
        self.grouped: bool = extra.get('group')
        self.master: bool = extra.get('master')
        self.open_direction: str = extra.get('open_direction')
