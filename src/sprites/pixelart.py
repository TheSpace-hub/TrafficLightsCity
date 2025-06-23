from typing import TYPE_CHECKING
import pygame as pg
from pygame import Surface, SRCALPHA

from src.sprite import Sprite

if TYPE_CHECKING:
    from src.game import Game


class Pixelart(Sprite):
    def __init__(self, game: 'Game', pos: tuple[int, int], pixel_size: int,
                 pixelart: tuple[tuple[tuple[int, int, int, int], ...]]):
        super().__init__(game, (0, 0), pos)
        self.game: 'Game' = game
        self.pixel_size: int = pixel_size
        self.pixelart: tuple[tuple[tuple[int, int, int, int], ...]] = pixelart

        self.update_view()

    def update_view(self):
        self.image = Surface((self.pixel_size * len(self.pixelart[0]), self.pixel_size * len(self.pixelart)), SRCALPHA,
                             32).convert_alpha()
        for y in range(len(self.pixelart)):
            for x in range(len(self.pixelart[y])):
                pg.draw.rect(self.image, self.pixelart[y][x], pg.Rect(
                    self.pixel_size * x, self.pixel_size * y, self.pixel_size, self.pixel_size
                ))

    def update(self):
        pass
