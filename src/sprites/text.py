import os.path
from typing import TYPE_CHECKING, Optional
import pygame as pg
from pygame import SRCALPHA

from src.sprite import Sprite

if TYPE_CHECKING:
    from src.game import Game


class TextAlign:
    CENTER = 0
    LEFT = 1
    RIGHT = 2

    @classmethod
    def apply(cls, method: int, text: 'Text'):
        if method == cls.CENTER:
            text.rect.x -= text.image.get_size()[0] / 2
            text.rect.y -= text.image.get_size()[1] / 2


class Text(Sprite):
    def __init__(self, game: 'Game', pos: tuple[int, int], text: str, font_size: int,
                 color: tuple[int, int, int, int] | tuple[int, int, int],
                 font_path: str = os.path.join('assets', 'fonts', 'MainFont.ttf'), align: int = TextAlign.CENTER,
                 max_wight: Optional[int] = None):
        super().__init__(game, (0, 0), pos)
        self.text: str = text
        self.game: 'Game' = game
        self.font_path: str = font_path
        self.font_size: int = font_size
        self.color: tuple[int, int, int, int] | tuple[int, int, int] = color
        self.align: int = align
        self.max_wight: Optional[int] = max_wight

        self.update_view()

        TextAlign.apply(align, self)

    def update_view(self):
        self.image = pg.Surface(self._get_surface_size(), SRCALPHA, 32).convert_alpha()
        for line, text in enumerate(self._get_lines()):
            self.image.blit(
                pg.font.Font(self.font_path, self.font_size).render(text, True, self.color),
                (0, line))

    def _get_lines(self) -> list[str]:
        return [self.text]

    def _get_line_height(self) -> int:
        return pg.font.Font(self.font_path, self.font_size).render('#', True, (0, 0, 0)).get_size()[1]

    def _get_surface_size(self) -> tuple[int, int]:
        wight = pg.font.Font(self.font_path, self.font_size).render(self.text, True, self.color).get_size()[0]
        if self.max_wight is not None and self.max_wight < wight:
            wight = self.max_wight

        height: int = self._get_line_height() * len(self._get_lines())

        return wight, height

    def update(self):
        pass
