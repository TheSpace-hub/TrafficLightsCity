import logging
from typing import TYPE_CHECKING
import json
import requests

from src.pinger.checker import Checker

if TYPE_CHECKING:
    from src.modules import TrafficLightData


class Pinger:
    def __init__(self, host: str = '127.0.0.1', port: int = 8081):
        self.host: str = host
        self.port: int = port
        self.traffic_lights_data: list['TrafficLightData'] = []
        self.running: bool = False
        self.checker = Checker()

    def add_traffic_light(self, traffic_light: 'TrafficLightData'):
        self.traffic_lights_data.append(traffic_light)

    def ping(self):
        for traffic_light in self.traffic_lights_data:
            self._ping_traffic_light(traffic_light)

    def _ping_traffic_light(self, data: 'TrafficLightData'):
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
            data.current_time += 1
            data.set_state(int(json.loads(response.content)['next_state']) - 1)
            data.note.set_level(None)
        except requests.exceptions.ConnectionError:
            logging.info('Не удалось соединиться с сервисом. (GET-запрос на url: %s). Учтено как 500-ка',
                         f'http://{self.host}:{self.port}/traffic')
            data.note.set_level(0)
