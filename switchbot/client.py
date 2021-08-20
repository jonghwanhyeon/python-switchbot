from typing import Any

import humps
import requests

switchbot_host = 'https://api.switch-bot.com/v1.0'


class SwitchBotClient:
    def __init__(self, token: str):
        self.session = requests.Session()
        self.session.headers['Authorization'] = token

    def request(self, method: str, path: str, **kwargs) -> Any:
        url = f'{switchbot_host}/{path}'
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
