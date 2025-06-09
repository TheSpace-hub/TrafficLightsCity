from typing import TYPE_CHECKING
from enum import Enum
import random
from math import sin, cos, radians

import pygame as pg

from src.sprite import Sprite

if TYPE_CHECKING:
    from src.game import Game


class TileTexture(Enum):
    GRASS = 0


class Tile(Sprite):
    def __init__(self, game: 'Game', x: int, y: int, size_x: int, size_y: int, pixel_size: int,
                 texture):
        print((size_x, pixel_size, cos(10)))
        super().__init__(game, (int(2 * size_x * pixel_size * cos(radians(20))),
                                int(2 * size_y * pixel_size * sin(radians(20)))),
                         (x, y))
        self.pixel_size: int = 0
        self.texture: TileTexture = texture

        self.update_view()

    def update_view(self):
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
                # pg.draw.rect(self.image, color, pg.Rect(x * 10, y * 10, 10, 10))
                pg.draw.polygon(self.image, (0, 255, 0), [
                    [self.image.get_size()[0] / 2, 0], [self.image.get_size()[0], self.image.get_size()[1] / 2],
                    [self.image.get_size()[0] / 2, self.image.get_size()[1]], [0, self.image.get_size()[1] / 2]
                ])

    def update(self):
        pass
