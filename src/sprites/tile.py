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

    @classmethod
    def get_one_of_colors(cls, texture: int) -> tuple[int, int, int]:
        if texture == TileTexture.GRASS.value:
            color = random.choice([
                (58, 140, 62),
                (94, 124, 22),
                (102, 162, 24),
                (58, 109, 53)
            ])
            return (
                min(255, max(0, color[0] + random.randint(-20, 20))),
                min(255, max(0, color[1] + random.randint(-20, 20))),
                min(255, max(0, color[2] + random.randint(-20, 20)))
            )
        return 255, 255, 255


class Tile(Sprite):
    """
    Клетка на поле
    Представляет собой ромб с углами _perspective_angle * 2 и (360 - _perspective_angle * 4) / 2
    """

    def __init__(self, game: 'Game', size: int, pixel_size: int,
                 texture: TileTexture, perspective_angle: int = 0):
        self.perspective_angle = perspective_angle
        super().__init__(game, (int(2 * size * pixel_size * cos(radians(self.perspective_angle))),
                                int(2 * size * pixel_size * sin(radians(self.perspective_angle)))),
                         (0, 0))
        self.size: int = size
        self.pixel_size: int = pixel_size
        self.texture: TileTexture = texture

        self.update_view()

    def update_view(self):
        for y in range(self.size):
            for x in range(self.size):
                self._draw_pixel(x, y)
        pg.draw.rect(self.image, (255, 255, 255), pg.Rect(0, 0, self.image.get_size()[0], self.image.get_size()[1]),
                     1)

    def _draw_pixel(self, x: int, y: int):
        start: tuple[float, float] = (
            x * self.pixel_size * sqrt(3) / 2 + y * self.pixel_size * sqrt(3) / 2,
            -x * self.pixel_size / 2 + y * self.pixel_size / 2
        )
        pg.draw.polygon(self.image, TileTexture.get_one_of_colors(0), [
            [start[0],
             start[1] + self.image.get_size()[1] / 2],
            [start[0] + self.pixel_size * sqrt(3) / 2,
             start[1] + self.image.get_size()[1] / 2 - self.pixel_size / 2],
            [start[0] + self.pixel_size * sqrt(3),
             start[1] + self.image.get_size()[1] / 2],
            [start[0] + self.pixel_size * sqrt(3) / 2,
             start[1] + self.image.get_size()[1] / 2 + self.pixel_size / 2]
        ])

    def update(self):
        pass
