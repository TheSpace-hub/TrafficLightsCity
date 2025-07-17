"""Модуль сцены с интро.
"""
from typing import TYPE_CHECKING
import pygame as pg
from math import sin
import time

from src.state import State

from src.sprites import Text

if TYPE_CHECKING:
    from src.game import Game


class Intro(State):
    """Класс интро.
    """
    def __init__(self, game: 'Game'):
        super().__init__(game)

    def boot(self):
        """Добавление основных спрайтов:
         - Имя.
         - Подсказка как продолжить.
         - Авторство.
        """
        self.add_sprite('name',
                        Text(self.game, (960, 540), 'Город светофоров',
                             48, (255, 255, 255)))
        self.add_sprite('tip',
                        Text(self.game, (960, 600), 'Нажмите любую клавишу чтобы продолжить',
                             18, (200, 200, 200)))

    def update(self):
        """Обновление каждый кадр.

        Изменение яркости текста.
        Переход в меню при нажатии клавиши.
        """
        tip: Text = self.get_sprite('tip')

        color: tuple[int, int, int] = tuple[int, int, int]([int(155 - (sin(time.time() * 2) * 100))] * 3)

        tip.color = color
        tip.update_view()

        if True in pg.key.get_pressed():
            self.game.change_state('Menu')

    def enter(self):
        pass

    def exit(self):
        pass
