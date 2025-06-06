"""
Основной класс игры.
Отвечает за цикл игры и изменение состояний.
"""
from typing import TYPE_CHECKING

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
        self.states: dict[str, 'State'] = {}
        self.current_state: 'State' | None = None

        self.screen: Surface = pg.display.set_mode((800, 800), pg.NOFRAME)
        self.clock: Clock = Clock()

        self.running: bool = True
        self.delta_time: float = 0

        pg.display.set_caption("Город светофоров")

    def loop(self):
        """
        Основной цикл игры
        """
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

        pg.quit()
