"""Dump details about all devices."""
import getpass
import os

from switchbot import SwitchBot


def _indentation(level):
    if level == 0:
        return ""

    return ("  " * level) + "- "


def _status(obj):
    type = obj.type

    if type == "Bot":
        if obj.mode == "toggle":
            return f" (state = {obj.state}, mode = {obj.mode})"
        else:
            return f" (mode = {obj.mode})"
    elif type == "CurtainGroup":
        return f" (position = {obj.position}%, fitting = {obj.fitting})"
    elif type == "Curtain":
        return f" (direction = {obj.direction}, moving = {obj.moving}, calibrated = {obj.calibrated}, battery = {obj.battery}%)"

    return ""


def _show(obj, level=0):
    print(f"{_indentation(level)}{obj.name}: {obj.type}{_status(obj)}")

    for child in obj.children:
        _show(child, level + 1)


def _dump(email, password):
    switchbot = SwitchBot(email)
    switchbot.authenticate(password)

    devices = switchbot.devices

    for device in devices:
        _show(device)


if __name__ == "__main__":
    email = os.environ.get("SWITCHBOT_EMAIL")
    password = os.environ.get("SWITCHBOT_PASSWORD")

    if not email:
        email = input("Email address: ")
    if not password:
        password = getpass.getpass()

    _dump(email, password)
