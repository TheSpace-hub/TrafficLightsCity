from typing import TYPE_CHECKING, Self
from enum import Enum
import random
from math import sin, cos, radians, sqrt

import pygame as pg

from src.sprite import Sprite

if TYPE_CHECKING:
    from src.game import Game


class TileTexture(Enum):
    GRASS = 0
    STONE = 1
    SAND = 2
    WATER = 3
    ASPHALT = 4

    @classmethod
    def get_one_of_colors(cls, texture: Self) -> tuple[int, int, int]:
        colors: dict[Self, list[tuple[int, int, int]]] = {
            TileTexture.GRASS: [
                (58, 140, 62),
                (94, 124, 22),
                (102, 162, 24),
                (58, 109, 53)
            ],
            TileTexture.STONE: [
                (90, 90, 90),
                (120, 120, 120),
                (60, 60, 60),
                (150, 150, 150)
            ],
            TileTexture.SAND: [
                (180, 165, 140),
                (160, 145, 120),
                (140, 125, 100),
                (120, 105, 80)
            ],
            TileTexture.WATER: [
                (100, 210, 220),
                (0, 150, 170),
                (70, 200, 200),
                (0, 105, 120)
            ],
            TileTexture.ASPHALT: [
                (50, 50, 50),
                (60, 55, 50),
                (30, 30, 30),
                (70, 65, 60)
            ]
        }
        color = random.choice(colors[texture])
        return (
            min(255, max(0, color[0] + random.randint(-10, 10))),
            min(255, max(0, color[1] + random.randint(-10, 10))),
            min(255, max(0, color[2] + random.randint(-10, 10)))
        )


class Tile(Sprite):
    """
    Клетка на поле
    Представляет собой ромб с углами _perspective_angle * 2 и (360 - _perspective_angle * 4) / 2
    """

    def __init__(self, game: 'Game', size: int, pixel_size: int,
                 texture: TileTexture, perspective_angle: int):
        self.perspective_angle = perspective_angle
        super().__init__(game, (round(2 * size * pixel_size * cos(radians(self.perspective_angle))),
                                round(2 * size * pixel_size * sin(radians(self.perspective_angle)))),
                         (0, 0))
        self.size: int = size
        self.pixel_size: int = pixel_size
        self.texture: TileTexture = texture

        self.update_view()

    def update_view(self):
        for y in range(self.size):
            for x in range(self.size):
                self._draw_pixel(x, y)

    def _draw_pixel(self, x: int, y: int):
        start: tuple[float, float] = (
            self.pixel_size * sqrt(3) * (x + y) / 2,
            self.pixel_size * (y - x) / 2
        )
        pg.draw.polygon(self.image, TileTexture.get_one_of_colors(self.texture), [
            [start[0],
             start[1] + self.image.get_size()[1] / 2],
            [start[0] + self.pixel_size * sqrt(3) / 2,
             start[1] + self.image.get_size()[1] / 2 - self.pixel_size / 2],
            [start[0] + self.pixel_size * sqrt(3),
             start[1] + self.image.get_size()[1] / 2],
            [start[0] + self.pixel_size * sqrt(3) / 2,
             start[1] + self.image.get_size()[1] / 2 + self.pixel_size / 2]
        ])

    @staticmethod
    def get_half_of_size(tile_size: int, pixel_size: int, perspective_angle: int, camera_distance: float) -> tuple[
        int, int]:
        return (round(tile_size * pixel_size * camera_distance / 10 * cos(radians(perspective_angle))),
                round(tile_size * pixel_size * camera_distance / 10 * sin(radians(perspective_angle))))

    def update(self):
        pass
