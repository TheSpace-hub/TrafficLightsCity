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

    def ping(self) -> dict[str, Optional[tuple[bool, str, int]]]:
        """Пинг всех светофоров на сервис.

        Returns:
            dict[str, Optional[tuple[bool, str, int]]]: Список всех светофоров с их ошибками.

        """
        results: dict[str, Optional[tuple[bool, str, int]]] = {}
        for data in self.traffic_lights_data:
            result: Optional[tuple[bool, str, int]] = self._ping_traffic_light(data)
            results[data.uuid] = result
            if result is None:
                logging.warning('Не удалось выполнить проверку светофора %s типа %s.',
                                data.uuid, data.tfl_type)
                data.note.set_level(5)
                data.note.note = f'Не удалось выполнить проверку светофора типа {data.tfl_type}.'
            elif 100 <= result[2] <= 299:
                logging.info('Проверка светофора %s прошла успешно.',
                             data.uuid)
                data.note.set_level(None)
                data.note.note = None
            elif result[2] == -1:
                logging.info('Не удалось соединиться с сервисом. (GET-запрос на url: %s).',
                             data.url)
                data.note.set_level(2)
                data.note.note = 'Не удалось соединиться с сервисом.'
            elif 500 <= result[2] <= 599:
                logging.error('При запросе светофора %s типа %s сервис упал с 500-ой ошибкой.',
                              data.uuid, data.tfl_type)
                data.note.set_level(4)
                data.note.note = result[1]
            elif not result[0]:
                logging.warning('Проверка светофора %s типа %s привела к ошибке "%s".',
                                data.uuid, data.tfl_type, result[1])
                data.note.set_level(4)
                data.note.note = result[1]
        return results

    def _ping_traffic_light(self, data: 'TrafficLightData') -> Optional[tuple[bool, str, int]]:
        """Пинг отдельного светофора.
        Args:
            data: Данные светофора

        Returns:
            Optional[tuple[bool, str, int]]:
                Если проверка невозможна, возвращает None, иначе, первым значением:
                - Если проверка пройдена, возвращает кортеж (True, "Успех")
                - Если проверка не пройдена, возвращает (False, "Причина ошибки")
                Вторым значением строка, которая описывает ошибку.
                Третьим значением статус код ответа.
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
            if 500 <= response.status_code <= 599:
                return False, 'Сервер упал с 500-ой ошибкой', response.status_code
            if 400 <= response.status_code <= 499:
                return False, 'Сервер вернул 400-ую ошибку', response.status_code

            data.current_time += 1
            data.set_state(int(json.loads(response.content)['next_state']) - 1)
            data.note.set_level(None)

            checking = self.checker.check(data.tfl_type, {
                'type': str(data.type_value),
                'data': {
                    'uuid': str(data.uuid),
                    'current_time': data.current_time,
                    'current_state': data.get_state() + 1
                }
            }, json.loads(response.content))
            if checking is None:
                return None
            return checking[0], checking[1], response.status_code
        except requests.exceptions.ConnectionError:
            return False, 'Сервер недоступен', -1
