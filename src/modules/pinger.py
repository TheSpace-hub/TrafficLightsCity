import json

import requests


class Pinger:
    def __init__(self, host: str = '127.0.0.1', port: int = 8081):
        self.host: str = host
        self.port: int = port

    def ping(self) -> tuple[int, dict]:
        response = requests.get(f'http://{self.host}:{self.port}/traffic', params={
            'type': '1',
            'data': json.dumps({
                'uuid': 'test',
                'current_time': 1,
                'current_state': 2
            })
        })
        return response.status_code, json.loads(response.content)
