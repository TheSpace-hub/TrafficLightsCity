from typing import TYPE_CHECKING
import json

import requests

if TYPE_CHECKING:
    from src.modules import TrafficLightData


class Pinger:
    def __init__(self, host: str = '127.0.0.1', port: int = 8081):
        self.host: str = host
        self.port: int = port
        self.traffic_lights_data: list['TrafficLightData'] = []
        self.current_time: int = 0
        self.running: bool = False

    def add_traffic_light(self, traffic_light: 'TrafficLightData'):
        self.traffic_lights_data.append(traffic_light)

    def ping(self) -> dict[str, tuple[int, dict]]:
        responses: dict[str, tuple[int, dict]] = {}
        for traffic_light in self.traffic_lights_data:
            responses[traffic_light.uuid] = self._ping_traffic_light(traffic_light)

        self.current_time += 1
        return responses

    def _ping_traffic_light(self, traffic_light: 'TrafficLightData') -> tuple[int, dict]:
        response = requests.get(f'http://{self.host}:{self.port}/traffic', params={
            'type': str(traffic_light.type_value),
            'data': json.dumps({
                'uuid': str(traffic_light.uuid),
                'current_time': traffic_light.current_time,
                'current_state': traffic_light.get_state() + 1
            })
        })
        traffic_light.current_time += 1
        traffic_light.set_state(int(json.loads(response.content)['next_state']) - 1)
        return response.status_code, json.loads(response.content)
