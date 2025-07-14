from typing import TYPE_CHECKING
import json

import requests

if TYPE_CHECKING:
    from src.modules import TrafficLightData


class Pinger:
    def __init__(self, host: str = '127.0.0.1', port: int = 8081):
        self.host: str = host
        self.port: int = port
        self.traffic_lights: list['TrafficLightData'] = []
        self.current_time: int = 0

    def add_traffic_light(self, traffic_light: 'TrafficLightData'):
        self.traffic_lights.append(traffic_light)

    def ping(self) -> dict[str, tuple[int, dict]]:
        print('ping')
        responses: dict[str, tuple[int, dict]] = {}
        for traffic_light in self.traffic_lights:
            responses[traffic_light.uuid] = self._ping_traffic_light(traffic_light)

        self.current_time += 1
        return responses

    def _ping_traffic_light(self, traffic_light: 'TrafficLightData') -> tuple[int, dict]:
        response = requests.get(f'http://{self.host}:{self.port}/traffic', params={
            'type': str(traffic_light.type_value),
            'data': json.dumps({
                'uuid': str(traffic_light.uuid),
                'current_time': self.current_time,
                'current_state': traffic_light.get_state()
            })
        })
        traffic_light.set_state(int(json.loads(response.content)['next_state']))
        return response.status_code, json.loads(response.content)
