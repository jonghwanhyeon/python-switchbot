# python-switchbot
A Python library to control SwitchBot devices connected to SwitchBot Hub

## Requirements
- Python 3.8+
- [pycognito](https://github.com/pvizeli/pycognito)
- [requests](https://requests.readthedocs.io)

## Installation
```python
pip install python-switchbot
```

## Usage
```python
from switchbot import SwitchBot

switchbot = SwitchBot('your@account.com')
switchbot.authenticate('yourpassword')

device = switchbot.device('AA:BB:CC:DD:EE:FF') # Device's BLE MAC
print(f'Current state: {device.state}')

# To turn off
device.turn('off') # -> device.state == 'off'

# To turn on
device.turn('on') # -> device.state == 'on'

# To toggle,
device.toggle()
```