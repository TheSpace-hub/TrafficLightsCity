"""Основной модуль игры 'Город светофоров'.

Реализует главный игровой цикл, управление состояниями (сценами) и отрисовку.

Модуль содержит:
- Класс Game - ядро игры, управляющее всеми процессами
- Настройку системы логирования
- Инициализацию pygame
- Механизм переключения между игровыми состояниями (сценами)

Основные функции:
- Запуск и остановка игры
- Обработка ввода (клавиатура, мышь)
- Обновление и отрисовка текущего состояния
- Управление временем кадров (delta time)
- Взаимодействие с сервером светофоров через Pinger
"""
import os
import logging
from typing import Any, TypeVar, Type, Optional

from colorlog import ColoredFormatter

import pygame as pg
from pygame import Surface
from pygame.time import Clock

from src.state import State
from src.pinger import Pinger

# Импорт НЕ УДАЛЯТЬ. Нужен чтобы все дочерние классы State были инициализированны
from src.states import *  # pylint: disable=wildcard-import

StateT = TypeVar('StateT', bound=State)


class Game:
    """Основной класс, управляющий игровым процессом.

    Отвечает за:
    - Главный игровой цикл
    - Управление состояниями (сценами)
    - Обработку ввода
    - Синхронизацию с сервером светофоров
    - Отрисовку игровых объектов

    Attributes:
        states (dict[str, State]): Словарь всех зарегистрированных состояний
        current_state (State | None): Текущее активное состояние
        transmitted_data (dict[str, Any]): Данные для передачи между состояниями
        screen (Surface): Основная поверхность для отрисовки
        clock (Clock): Таймер для контроля FPS
        omitted_buttons (list[int]): Список пропущенных нажатий клавиш
        omitted_mouse_buttons (list[int]): Список пропущенных нажатий мыши
        is_mouse_move (bool): Флаг движения мыши
        running (bool): Флаг работы игрового цикла
        delta_time (float): Время между кадрами (в секундах)
        lock_mouse (bool): Флаг блокировки курсора мыши
        _previous_mouse_location (tuple[int, int]): Предыдущая позиция мыши
        mouse_offset (tuple[int, int]): Смещение мыши с последнего кадра
        pinger (Pinger): Клиент для взаимодействия с сервером светофоров
        last_ping_time (float): Время последнего ping-запроса
    """

    def __init__(self):
        Game.configure_logs()
        pg.init()
        pg.font.init()

        self.states: dict[str, 'State'] = {}
        self.current_state: 'State' | None = None
        self.transmitted_data: dict[str, Any] = {}

        self.screen: Surface = pg.display.set_mode((1920, 1080))
        self.clock: Clock = Clock()

        self.omitted_buttons: list[int] = []
        self.omitted_mouse_buttons: list[int] = []
        self.is_mouse_move: bool = False

        self.running: bool = True
        self.delta_time: float = 0

        self.lock_mouse: bool = False
        self._previous_mouse_location: tuple[int, int] = (0, 0)
        self.mouse_offset: tuple[int, int] = (0, 0)

        self.pinger: Pinger = Pinger()
        self.last_ping_time: float = 0

        pg.display.set_caption('Город светофоров')

        self.init_states()

    def loop(self):
        """Запускает главный игровой цикл.

        Обрабатывает:
        - События pygame (выход, ввод с клавиатуры/мыши)
        - Обновление состояния игры
        - Отрисовку кадра
        """
        while self.running:
            self.omitted_buttons = []
            self.omitted_mouse_buttons = []
            self.is_mouse_move = False
            self.mouse_offset = (0, 0)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    self.omitted_buttons.append(event.key)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.omitted_mouse_buttons.append(event.button)
                if event.type == pg.MOUSEMOTION:
                    self.is_mouse_move = True
                    self.mouse_offset = (pg.mouse.get_pos()[0] - self._previous_mouse_location[0],
                                         pg.mouse.get_pos()[1] - self._previous_mouse_location[1])
                    if self.lock_mouse:
                        pg.mouse.set_pos(self._previous_mouse_location)
                    else:
                        self._previous_mouse_location = pg.mouse.get_pos()
            self.delta_time = self.clock.tick(60) / 1000

            self.update()

        pg.quit()

    def update(self):
        """Выполняет обновление игрового состояния текущей сцены.

        Обновляет:
        - Логику текущего состояния (сцены)
        - Все зарегистрированные спрайты сцены
        - Отображение (через update_view())
        """
        if self.current_state:
            self.current_state.update()
            for sprite in list(self.current_state.sprites.values()):
                sprite.update()

        self.update_view()

    def update_view(self):
        """Отрисовывает все объекты на сцене.
        """
        x_factor = pg.display.get_window_size()[0] / 1920
        y_factor = pg.display.get_window_size()[1] / 1080
        self.screen.fill((32, 32, 32))
        for sprite in self.current_state.sprites.values():
            self.screen.blit(sprite.image,
                             pg.Rect(sprite.rect.x * x_factor, sprite.rect.y * y_factor, 0, 0))
        pg.display.flip()

    def init_states(self):
        """Инициализировать сцены по умолчанию.
        """
        for state in State.__subclasses__():
            self.register_state(state)

    def register_state(self, state: Type[StateT]):
        """Регистрация новой сцены.

        Args:
            state (Type[StateT]): Класс-наследник абстрактного State.

        Note:
            Вызывает функцию boot().
        """
        self.states[str(state.__name__)] = state(self)
        self.states[str(state.__name__)].boot()

    def change_state(self, state: str, transmitted_data: Optional[dict[str, Any]] = None):
        """Переключает текущее активное состояние игры на указанное.

        Args:
            state: Название состояния для переключения (должно быть зарегистрировано
                   через register_state()). Регистрозависимая строка.
            transmitted_data: Данные для передачи в новое состояние. Будут доступны
                             через self.transmitted_data в методе enter() нового состояния.
                             По умолчанию None (используется пустой словарь).

        Side Effects:
            - Изменяет self.current_state
            - Временно изменяет self.transmitted_data
            - Вызывает методы exit() и enter() у состояний
            - Логирует ошибки при отсутствии состояния

        Note:
            - transmitted_data очищается после вызова enter()
            - Для корректной работы состояние должно быть предварительно зарегистрировано
            - Метод безопасен для вызова (не выбрасывает исключения при ошибках)

        Example:
            >>> game.change_state("MainMenu", {"show_intro": True})
            >>> game.current_state.__class__.__name__
            'MainMenu'
        """
        if transmitted_data is None:
            transmitted_data = {}
        if state not in self.states:
            logging.error('Сцена с названием %s не зарегистрирована.', state)
            return

        if self.current_state is not None:
            self.current_state.exit()

        self.current_state = self.states[state]
        self.transmitted_data = transmitted_data
        self.current_state.enter()
        self.transmitted_data = {}

    def quit(self):
        """Завершение игрового цикла
        """
        self.running = False

    @staticmethod
    def configure_logs():
        """
        Настройка логов.
        Определяет место записи и определяет цвет логов.
        """
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
        logging.getLogger('werkzeug').disabled = True

        log_format = '[%(asctime)s][%(levelname)s] %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'

        handlers = [
            logging.FileHandler(
                os.path.join('logs', 'server.stderr'),
                encoding='utf-8',
                mode='w'),
            logging.StreamHandler()
        ]

        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            datefmt=date_format,
            handlers=handlers
        )

        root_logger = logging.getLogger()

        console_formatter = ColoredFormatter(
            fmt='%(log_color)s' + log_format + '%(reset)s',
            datefmt=date_format,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'white',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )

        for handler in root_logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                handler.setFormatter(console_formatter)
