"""Файл для дополнительной проверки запросов со светофора.
"""

from typing import Optional

from src.pinger import Checker

checker = Checker()


@checker('basic')
def check_basic(request: dict, response: dict) -> tuple[bool, Optional[str]]:
    """
    Пример проверки запроса на 3-х сегментный светофор и ответа.

    Args:
        request (dict): Словарь, отправленный долбилкой
        response (dict):  Словарь, возвращённый с сервиса

    Returns:
        tuple[bool, str]: Кортеж, где:
            - bool: Результат проверки (True — успех, False — ошибка).
            - str | None: Описание ошибки (Используйте None для отсутствия параметра)
    """

    return True, None


@checker('arrow')
def check_arrow(request: dict, response: dict) -> tuple[bool, Optional[str]]:
    """
    Пример проверки запроса на 3-х сегментный светофор со стрелкой и ответа.

    Args:
        request (dict): Словарь, отправленный долбилкой
        response (dict):  Словарь, возвращённый с сервиса

    Returns:
        tuple[bool, str]: Кортеж, где:
            - bool: Результат проверки (True — успех, False — ошибка).
            - str | None: Описание ошибки (Используйте None для отсутствия параметра)
    """

    return True, None


@checker('pedestrian_crossing')
def check_pedestrian_crossing(request: dict, response: dict) -> tuple[bool, Optional[str]]:
    """
    Пример проверки запроса на светофор для пешеходного перехода и ответа.

    Args:
        request (dict): Словарь, отправленный долбилкой
        response (dict):  Словарь, возвращённый с сервиса

    Returns:
        tuple[bool, str]: Кортеж, где:
            - bool: Результат проверки (True — успех, False — ошибка).
            - str | None: Описание ошибки (Используйте None для отсутствия параметра)
    """

    return True, None
