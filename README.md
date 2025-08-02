# Город светофоров для курса DevOps

<p align="center">
    <a href="https://github.com/charmbracelet/crush/releases"><img src="https://img.shields.io/github/v/release/TheSpace-hub/TrafficLightsCity" alt="Latest Release"></a>
    <a href="https://github.com/charmbracelet/crush/releases"><img src="https://img.shields.io/github/actions/workflow/status/TheSpace-hub/TrafficLightsCity/pylint.yml?style=flat-square&label=Pylint" alt="Pylint"></a>
    <a href="https://github.com/charmbracelet/crush/actions"><img src="https://github.com/TheSpace-hub/TrafficLightsCity/workflows/build/badge.svg" alt="Build Status"></a>
</p>

Долбилка в продакшн с GUI интерфейсом

## Технологический стек

| Технология    | Windows                                       | Linux                              |
|---------------|-----------------------------------------------|------------------------------------|
| Python: 3.13+ | [Оф. Сайт](https://www.python.org/downloads/) | `sudo apt install python3.13`      |
| Python: 3.13+ | -                                             | `sudo apt install python3.13-venv` |
| Tkinter       | -                                             | `sudo apt install python3.13-tk`   |
| Pillow        | `pip install pillow`                          | `pip3 install pillow`              |
| NumPy         | `pip install numpy`                           | `pip3 install numpy`               |

## Создание города

### Создание карты города

В меню нажмите кнопку `Создать город`, опционально введите seed, затем нажмите на кнопку `Создать новый город`, после
чего автоматически будет создана карта города с дорогами, на которых можно разместить светофоры.

## Авто-проверка ошибок

Для создания логики проверки перейдите в `check/master`, создайте функцию, затем повесьте на функцию декоратор
`@checker`, указав в качестве входных данных, какой тип светофора проверяет функция.

Пример функции, которая возвращает ошибку, если стадия больше 3-х.

```py
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
    if request['data']['current_state'] > 1:
        return False, f'Стадии под индексом {request['data']['current_state']} не существует.'
    return True, None
```

### Lite-версия

Базовая проверка включает в себя проверку на доступность сервиса и корректность возвращаемой с него информации. В
lite-версии код из `check/master.py` собирается в бинарник и отключает предупреждение о том, что на светофор нет
проверки в файле.

Чтобы запустить lite-версию, скачайте билд из релиза, распакуйте архив и запустите `TrafficLightsCity`. Файл .exe-шник
на Windows, бинарник на Linux.
---
Для запуска на Linux выдайте права на запуск и запустите бинарник.

```bash
chmod +x ./TrafficLightsCityLite
./
```