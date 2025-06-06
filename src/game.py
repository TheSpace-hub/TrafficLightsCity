"""
Основной класс игры.
Отвечает за цикл игры и изменение состояний.
"""
from typing import TYPE_CHECKING, Type

import os
import logging

from colorlog import ColoredFormatter

import pygame as pg
from pygame import Surface
from pygame.time import Clock

if TYPE_CHECKING:
    from src.state import State


class Game:
    """
    Основной класс игры
    """

    def __init__(self):
        self.states: dict[Type['State'], 'State'] = {}
        self.current_state: 'State' | None = None

        self.screen: Surface = pg.display.set_mode((800, 800), pg.NOFRAME)
        self.clock: Clock = Clock()

        self.running: bool = True
        self.delta_time: float = 0

        pg.display.set_caption('Город светофоров')

        Game.configure_logs()

    def loop(self):
        """
        Основной цикл игры
        """
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

        pg.quit()

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
