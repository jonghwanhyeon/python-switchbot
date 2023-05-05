from enum import Enum

class AirConditionerMode(Enum):
    AUTO = 1
    COOL = 2
    DRY = 3
    FAN = 4
    HEAT = 5

class AirConditionerFanSpeed(Enum):
    AUTO = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4

class AirConditionerPowerState(Enum):
    ON = "on"
    OFF = "off"