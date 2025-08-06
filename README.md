# Город светофоров 🚦
<p align="center">
    <img width="1915" height="1079" alt="preview" src="https://github.com/user-attachments/assets/cc855d0c-771f-400e-a3b8-22080c38c632" />
</p>

---

<p align="center">
    <a href="https://github.com/TheSpace-hub/TrafficLightsCity/releases"><img src="https://img.shields.io/github/v/release/TheSpace-hub/TrafficLightsCity?style=flat-square" alt="Latest Release"></a>
    <a href="https://github.com/TheSpace-hub/TrafficLightsCity/actions"><img src="https://img.shields.io/github/actions/workflow/status/TheSpace-hub/TrafficLightsCity/build.yml?style=flat-square&label=Build" alt="Build Status"></a>
    <a href="https://github.com/TheSpace-hub/TrafficLightsCity?tab=GPL-3.0-1-ov-file"><img src="https://img.shields.io/github/license/TheSpace-hub/TrafficLightsCity?style=flat-square" alt="License"></a>
</p>

Приложение с графическим интерфейсом для моделирования и тестирования работы сервиса обрабатывающего светофоры.

## Технологический стек

### Основные зависимости

| Компонент    | Установка (Windows)                                   | Установка (Linux)                  |
|--------------|-------------------------------------------------------|------------------------------------|
| Python 3.13+ | [Официальный сайт](https://www.python.org/downloads/) | `sudo apt install python3.13`      |
| Python venv  | Включено в стандартную установку Python               | `sudo apt install python3.13-venv` |
| Tkinter      | Включено в стандартную установку Python               | `sudo apt install python3.13-tk`   |

### Дополнительные библиотеки

```bash
pip install colorlog pygame pillow requests
```

## Установка

### Способ 1: Готовые сборки

1. Перейдите в [раздел релизов](https://github.com/TheSpace-hub/TrafficLightsCity/releases)
2. Скачайте архив для вашей ОС
3. Распакуйте архив
4. Запустите:
    - Windows: `TrafficLightsCity.exe`
    - Linux: `./TrafficLightsCity` (предварительно выполните `chmod +x TrafficLightsCity`)

### Способ 2: Исходный код

```bash
git clone https://github.com/TheSpace-hub/TrafficLightsCity.git
cd TrafficLightsCity
pip install -r requirements.txt  # Установка зависимостей
python main.py                   # Запуск приложения
```

## Использование

1. Запустите приложение
2. Нажмите "Создать город"
3. (Опционально) Введите seed для генерации
4. Нажмите "Создать новый город"
5. На сгенерированной карте разместите светофоры

## Разработка проверок

Для создания собственных проверок светофоров:

1. Перейдите в `check/master.py`
2. Создайте функцию проверки
3. Добавьте декоратор `@checker` с указанием типа светофора

### Пример проверки

```python
@checker('basic')
def check_basic(request: dict, response: dict) -> tuple[bool, str | None]:
    """
    Проверяет корректность состояния светофора
    
    Args:
        request: Данные запроса к светофору
        response: Ответ от светофора
        
    Returns:
        Кортеж (результат проверки, сообщение об ошибке)
    """
    if request['data']['current_state'] > 1:
        return False, f'Стадии под индексом {request["data"]["current_state"]} не существует.'
    return True, None
```

## Lite-версия

Lite-версия включает:

- Базовые проверки доступности сервиса
- Проверку корректности ответов
- Предварительно скомпилированные проверки

Для запуска Lite-версии используйте файлы из раздела релизов.

### Особенности:

- Не требует установки зависимостей
- Не поддерживает кастомные проверки
- Имеет предупреждение об отсутствии проверок для светофоров
