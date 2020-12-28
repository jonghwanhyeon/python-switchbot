"""Utility functions."""
import re


def url_for(key):
    """Return URL for request type."""
    return {
        "query_user": "https://l9ren7efdj.execute-api.us-east-1.amazonaws.com/developStage/user/v1",
        "get_devices": "https://l9ren7efdj.execute-api.us-east-1.amazonaws.com/developStage/sortdevices/v1/devices",
        "get_device": "https://l9ren7efdj.execute-api.us-east-1.amazonaws.com/developStage/device/v1/getdevice",
        "device_data": "https://l9ren7efdj.execute-api.us-east-1.amazonaws.com/developStage/devicedata/v1/getdata",
        "refresh_device": "https://l9ren7efdj.execute-api.us-east-1.amazonaws.com/developStage/devicestatus/v1/getstatus",
        "turn_device": "https://vxhewp40e8.execute-api.us-east-1.amazonaws.com/beta/v1/action",
    }.get(key)


def sanitize_id(dirty_id):
    """Convert ID to sanitised version."""
    clean_id = dirty_id.upper()
    clean_id = re.sub(r"[^A-F0-9]", "", clean_id)
    return clean_id
