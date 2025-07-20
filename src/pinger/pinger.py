import logging
from typing import TYPE_CHECKING, Optional
import json
import requests

from src.pinger.checker import Checker

if TYPE_CHECKING:
    from src.modules import TrafficLightData


class Pinger:
    def __init__(self):
        self.traffic_lights_data: list['TrafficLightData'] = []
        self.running: bool = False
        self.checker = Checker()

    def add_traffic_light(self, traffic_light: 'TrafficLightData'):
        self.traffic_lights_data.append(traffic_light)

    def ping(self):
        for data in self.traffic_lights_data:
            result: tuple[bool, str] | None = self._ping_traffic_light(data)
            if result is None:
                logging.error('Не удалось выполнить проверку светофора %s типа %s.',
                              data.uuid, data.tfl_type)
                data.note.set_level(3)
                data.note.note = 'Не удалось выполнить проверку светофора типа ' + data.tfl_type
            elif result[0]:
                logging.info('Проверка светофора %s прошла успешно.',
                             data.uuid)
                data.note.set_level(None)
            elif not result[0] and result[1] == 'Сервер недоступен':
                logging.info('Не удалось соединиться с сервисом. (GET-запрос на url: %s).',
                             data.url)
                data.note.set_level(2)
                data.note.note = 'Не удалось соединиться с сервисом.'
            elif not result[0]:
                logging.warning('Проверка светофора %s привела к ошибке "%s".',
                                data.uuid, result[1])
                data.note.set_level(0)
                data.note.note = result[1]

    def _ping_traffic_light(self, data: 'TrafficLightData') -> Optional[tuple[bool, str]]:
        """Пинг отдельного светофора.
        Args:
            data: Данные светофора

        Returns:
            Optional[tuple[bool, str]]:
                - Если проверка пройдена, возвращает кортеж (True, "Успех")
                - Если проверка не пройдена, возвращает (False, "Причина ошибки")
                - Если проверка невозможна, возвращает None
        """
        try:
            response = requests.get(data.url, params={
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

            return self.checker.check(data.tfl_type, {
                'type': str(data.type_value),
                'data': {
                    'uuid': str(data.uuid),
                    'current_time': data.current_time,
                    'current_state': data.get_state() + 1
                }
            }, json.loads(response.content))
        except requests.exceptions.ConnectionError:
            return False, 'Сервер недоступен'
