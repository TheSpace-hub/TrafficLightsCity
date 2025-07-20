from typing import TYPE_CHECKING
from random import uniform
from math import pi, sqrt, ceil

import pygame as pg
from pygame import SRCALPHA

from src.sprites import Pixelart
from src.sprite import Sprite

if TYPE_CHECKING:
    from src.game import Game


class Jumper(Sprite):
    def __init__(self, game: 'Game', pos: tuple[int, int], size: tuple[int, int],
                 pixelart: tuple[tuple[tuple[int, int, int, int], ...]]):
        super().__init__(game, (int(size[0] * sqrt(2)), int(size[1] * 2 * sqrt(2))), pos)
        self.pixelart: tuple[tuple[tuple[int, int, int, int], ...]] = pixelart
        self.index: int = 0
        self.angle = uniform(-45, 45)

    def update_view(self):
        self.image = pg.Surface(self.image.get_size(), SRCALPHA, 32).convert_alpha()

        surface = pg.Surface((30, 30), SRCALPHA, 32).convert_alpha()
        pixel_size: float = min(30 / len(self.pixelart[0]), 30 / len(self.pixelart[1]))
        alpha = 255 - self.index * 255 / sqrt(2)
        for y in range(len(self.pixelart)):
            for x in range(len(self.pixelart[y])):
                color = (
                    self.pixelart[y][x][0],
                    self.pixelart[y][x][1],
                    self.pixelart[y][x][2],
                    min(self.pixelart[y][x][3], alpha)
                )
                pg.draw.rect(surface, color, pg.Rect(
                    pixel_size * x, pixel_size * y, ceil(pixel_size), ceil(pixel_size)
                ))

        self.image.blit(pg.transform.rotate(surface, self.angle),
                        (0, 43 - self.index * 30 / sqrt(2)))

    def update(self):
        if self.index < sqrt(2):
            self.update_view()
            self.index += .05
