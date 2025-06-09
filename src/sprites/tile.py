from typing import TYPE_CHECKING
from enum import Enum
import random
from math import sin, cos, radians, sqrt

import pygame as pg

from src.sprite import Sprite

if TYPE_CHECKING:
    from src.game import Game


class TileTexture(Enum):
    GRASS = 0


class Tile(Sprite):
    """
    Клетка на поле
    Представляет собой ромб с углами _perspective_angle * 2 и (360 - _perspective_angle * 4) / 2
    """

    def __init__(self, game: 'Game', x: int, y: int, size_x: int, size_y: int, pixel_size: int,
                 texture):
        self._perspective_angle = 30
        super().__init__(game, (int(2 * size_x * pixel_size * cos(radians(self._perspective_angle))),
                                int(2 * size_y * pixel_size * sin(radians(self._perspective_angle)))),
                         (x, y))
        self.pixel_size: int = pixel_size
        self.texture: TileTexture = texture

        self.update_view()

    def update_view(self):
        pg.draw.polygon(self.image, (255, 255, 255), [
            [self.image.get_size()[0] / 2, 0], [self.image.get_size()[0], self.image.get_size()[1] / 2],
            [self.image.get_size()[0] / 2, self.image.get_size()[1]], [0, self.image.get_size()[1] / 2]
        ])
        pg.draw.polygon(self.image, (0, 0, 0), [
            [self.image.get_size()[0] / 2, 1], [self.image.get_size()[0] - 1, self.image.get_size()[1] / 2],
            [self.image.get_size()[0] / 2, self.image.get_size()[1] - 1], [1, self.image.get_size()[1] / 2]
        ])
        for y in range(10):
            for x in range(10):
                color = random.choice([
                    (58, 140, 62),
                    (94, 124, 22),
                    (102, 162, 24),
                    (58, 109, 53)
                ])
                color = (
                    min(255, max(0, color[0] + random.randint(-20, 20))),
                    min(255, max(0, color[1] + random.randint(-20, 20))),
                    min(255, max(0, color[2] + random.randint(-20, 20)))
                )
                pg.draw.polygon(self.image, (0, 255, 0), [
                    [0, self.image.get_size()[1] / 2],
                    [self.pixel_size * sqrt(3) / 2, self.image.get_size()[1] / 2 - self.pixel_size / 2],
                    [self.pixel_size * sqrt(3), self.image.get_size()[1] / 2],
                    [self.pixel_size * sqrt(3) / 2, self.image.get_size()[1] / 2 + self.pixel_size / 2]
                ])

    def update(self):
        pass
