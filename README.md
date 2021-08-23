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
your_switch_bot_token = '98a6732b2ac256d40ffab7db31a82f518969f4d1a64eadff581d45e902327b7c577aa6ead517bda589c19b4ca0b2599b'
switchbot = SwitchBot(token=your_switch_bot_token)

# To list all devices
devices = switchbot.devices()
for device in devices:
    print(device)
# Bot(id=CD0A18B1C291)
# HubMini(id=4CAF08629A21)
# Bot(id=5F0B798AEF91)

# If you already know a device id:
device = switchbot.device(id='5F0B798AEF91')
# Device(id=5F0B798AEF91)

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
