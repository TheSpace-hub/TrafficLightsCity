"""
Текст
"""
import os.path
from typing import TYPE_CHECKING
import pygame as pg

from src.sprite import Sprite

if TYPE_CHECKING:
    from src.game import Game


class TextAlign:
    """
    Расположение текста относительно координат
    """
    CENTER = 0
    LEFT = 1
    RIGHT = 2

    @classmethod
    def apply(cls, method: int, text: 'Text'):
        if method == cls.CENTER:
            text.rect.x -= text.image.get_size()[0] / 2
            text.rect.y -= text.image.get_size()[1] / 2


class Text(Sprite):
    """
    Текст
    """

    def __init__(self, game: 'Game', pos: tuple[int, int], text: str, font_size: int,
                 color: tuple[int, int, int, int] | tuple[int, int, int],
                 font_path: str = os.path.join('assets', 'fonts', 'MainFont.ttf'), align: int = TextAlign.CENTER
                 ):
        super().__init__(game, (0, 0), pos)
        self.text: str = text
        self.game: 'Game' = game
        self.font_path: str = font_path
        self.font_size: int = font_size
        self.color: tuple[int, int, int, int] | tuple[int, int, int] = color
        self.align: int = align

        self.update_view()

        TextAlign.apply(align, self)

    def update_view(self):
        """
        Обновление изображения
        """
        self.image = pg.font.Font(self.font_path, self.font_size).render(self.text, True, self.color)

    def update(self):
        pass
