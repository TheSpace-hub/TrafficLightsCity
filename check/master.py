from src.pinger import Checker

checker = Checker()


@checker('basic')
def check_basic(request: dict, response: dict) -> tuple[bool, str | None]:
    """
    Пример проверки запроса на светофор и ответа.

    Args:
        request (dict): Словарь, отправленный долбилкой
        response (dict):  Словарь, возвращённый с сервиса

    Returns:
        tuple[bool, str]: Кортеж, где:
            - bool: Результат проверки (True — успех, False — ошибка).
            - str | None: Описание ошибки (Используйте None для отсутствия параметра)
    """

    print(f'Req: {request}; Res: {response}')
    return False, 'Тестовая ошибка'
