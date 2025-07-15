import logging
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
        try:
            requests.get(f'http://{self.host}:{self.port}/traffic')
        except requests.exceptions.ConnectionError:
            logging.warning('Не удалось соединиться с сервисом. (GET-запрос на url: %s).',
                            f'http://{self.host}:{self.port}/traffic')
            return {}
        responses: dict[str, tuple[int, dict]] = {}
        for traffic_light in self.traffic_lights_data:
            responses[traffic_light.uuid] = self._ping_traffic_light(traffic_light)

        self.current_time += 1
        return responses

    def _ping_traffic_light(self, data: 'TrafficLightData') -> tuple[int, dict]:
        """Пинг отдельного светофора.
        Args:
            data: Данные светофора

        """
        try:
            response = requests.get(f'http://{self.host}:{self.port}/traffic', params={
                'type': str(data.type_value),
                'data': json.dumps({
                    'uuid': str(data.uuid),
                    'current_time': data.current_time,
                    'current_state': data.get_state() + 1
                })
            })
        except requests.exceptions.ConnectionError:
            logging.info('Не удалось соединиться с сервисом. (GET-запрос на url: %s). Учтено как 500-ка',
                         f'http://{self.host}:{self.port}/traffic')
            return 500, {}
        data.current_time += 1
        data.set_state(int(json.loads(response.content)['next_state']) - 1)
        return response.status_code, json.loads(response.content)
