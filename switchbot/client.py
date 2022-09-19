from typing import Any

import humps
import requests
import time
import hashlib
import hmac
import base64

switchbot_hosts = {
        '1.0': 'https://api.switch-bot.com/v1.0', 
        '1.1': 'https://api.switch-bot.com/v1.1'
    }

class SwitchBotClient:
    def legacy_setup(self, token: str):
        self.ver = "1.0"
        self.session.headers['Authorization'] = token

    def __init__(self, token: str, ver: str = None, secret: str = None, nonce: str = None):
        self.session = requests.Session()

        # base case regular 1.0 API / defaults
        if ver == None or secret == None or nonce == None:
            self.legacy_setup(token)
            return

        self.ver = ver

        t = int(round(time.time() * 1000))
        string_to_sign = '{}{}{}'.format(token, t, nonce)
        string_to_sign = bytes(string_to_sign, 'utf-8')

        secret = bytes(secret, 'utf-8')

        sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

        self.session.headers['sign'] = sign
        self.session.headers['Authorization'] = token
        self.session.headers['nonce'] = nonce
        self.session.headers['t'] = '{}'.format(t)

    def request(self, method: str, path: str, **kwargs) -> Any:
        url = f'{switchbot_hosts[self.ver]}/{path}'
        response = self.session.request(method, url, **kwargs)

        if response.status_code != 200:
            raise RuntimeError(
                f'SwitchBot API server returns status {response.status_code}')

        response_in_json = humps.decamelize(response.json())
        if response_in_json['status_code'] != 100:
            raise RuntimeError(
                f'An error occurred: {response_in_json["message"]}')

        return response_in_json

    def get(self, path: str, **kwargs) -> Any:
        return self.request('GET', path, **kwargs)

    def post(self, path: str, **kwargs) -> Any:
        return self.request('POST', path, **kwargs)

    def put(self, path: str, **kwargs) -> Any:
        return self.request('PUT', path, **kwargs)

    def delete(self, path: str, **kwargs) -> Any:
        return self.request('DELETE', path, **kwargs)
