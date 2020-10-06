def url_for(key):
    return {
        'query_user': 'https://l9ren7efdj.execute-api.us-east-1.amazonaws.com/developStage/user/v1',
        'refresh_device': 'https://l9ren7efdj.execute-api.us-east-1.amazonaws.com/developStage/devicestatus/v1/getstatus',
        'turn_device': 'https://vxhewp40e8.execute-api.us-east-1.amazonaws.com/beta/v1/action',
    }.get(key)