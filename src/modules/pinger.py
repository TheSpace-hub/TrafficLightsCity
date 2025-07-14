import requests


class Pinger:
    def __init__(self, host: str = '127.0.0.1', port: int = 8081):
        self.host: str = host
        self.port: int = port

    def ping(self):
        requests.get(f'http://{self.host}:{self.port}/traffic', params={
            'a': 1
        })
