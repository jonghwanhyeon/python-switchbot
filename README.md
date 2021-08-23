# python-switchbot
A Python library to control SwitchBot devices connected to SwitchBot Hub

## Requirements
- Python 3.8+
- [A SwitchBot Token](https://github.com/OpenWonderLabs/SwitchBotAPI#getting-started)

## Installation
```python
pip install python-switchbot
```

## Usage
```python
from switchbot import SwitchBot

# To get the token, please refer to https://github.com/OpenWonderLabs/SwitchBotAPI#getting-started
your_switch_bot_token = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
switchbot = SwitchBot(token=your_switch_bot_token)

# To list all devices
devices = switchbot.devices()
for device in devices:
    print(device)
# Bot(id=0A1B2C3D4E5F)
# HubMini(id=F0A5E1B4D2C3)
# Bot(id=F5E4D3C2B1A0)

# If you already know a device id:
device = switchbot.device(id='F5E4D3C2B1A0')
# Device(id=F5E4D3C2B1A0)

# To query a status of a device
print(device.status())
# {'power': 'off'}

# To command actions,
device.command('turn_on')
device.command('turn_off')
device.command('press')
device.command('set_position', parameter='0,ff,80)
```

## Contributors
Thanks to all contributors!
- [Stuart Clark](https://github.com/stuart-c)
