"""
Основной класс игры.
Отвечает за цикл игры и изменение состояний.
"""
import os
import logging
from typing import Any

from colorlog import ColoredFormatter

import pygame as pg
from pygame import Surface
from pygame.time import Clock

from src.state import State

from src.states import *  # Импорт НЕ УДАЛЯТЬ. Нужен чтобы все дочерние классы State были инициализированны


class Game:
    """
    Основной класс игры
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

        self.running: bool = True
        self.delta_time: float = 0

        self.lock_mouse: bool = False
        self._previous_mouse_location: tuple[int, int] = (0, 0)
        self.mouse_offset: tuple[int, int] = (0, 0)
        pg.display.set_caption('Город светофоров')

        self.init_states()

    def loop(self):
        """
        Основной цикл игры
        """
        while self.running:
            self.omitted_buttons = []
            self.omitted_mouse_buttons = []
            self.mouse_offset = (0, 0)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    self.omitted_buttons.append(event.key)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.omitted_mouse_buttons.append(event.button)
                if event.type == pg.MOUSEMOTION:
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
        """
        Обновляет текущую сцену
        """
        if self.current_state:
            self.current_state.update()
            for sprite in list(self.current_state.sprites.values()):
                sprite.update()

        self.update_view()

    def update_view(self):
        """
        Обновляет экран
        """
        x_factor = pg.display.get_window_size()[0] / 1920
        y_factor = pg.display.get_window_size()[1] / 1080
        self.screen.fill((32, 32, 32))
        for sprite in self.current_state.sprites.values():
            self.screen.blit(sprite.image, pg.Rect(sprite.rect.x * x_factor, sprite.rect.y * y_factor, 0, 0))
        pg.display.flip()

    def init_states(self):
        """
        Добавить все сцены
        """
        for state in State.__subclasses__():
            self.register_state(state)

    def register_state(self, state):
        """
        Добавление сцен
        :param state: Объект сцены
        """
        self.states[str(state.__name__)] = state(self)
        self.states[str(state.__name__)].boot()

    def change_state(self, state: str, transmitted_data: dict[str, Any] = None):
        """
        Изменить сцену
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
        self.running = False

    @staticmethod
    def configure_logs():
        """
        Настройка логов.
        Определяет место записи и цвет логов цветными.
        """
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
        logging.getLogger('werkzeug').disabled = True

        log_format = f'[%(asctime)s][%(levelname)s] %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'

        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            datefmt=date_format
        )

        handlers = [
            logging.FileHandler(
                os.path.join('logs', 'server.stderr'),
                encoding='utf-8',
                mode='w'),
            logging.StreamHandler()
        ]

        logging.basicConfig(
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
