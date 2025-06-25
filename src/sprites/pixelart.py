from typing import TYPE_CHECKING
from math import ceil
import pygame as pg
from pygame import Surface, SRCALPHA
from PIL import Image

from src.sprite import Sprite

if TYPE_CHECKING:
    from src.game import Game


class Pixelart(Sprite):
    def __init__(self, game: 'Game', pos: tuple[int, int], max_size: tuple[int, int],
                 pixelart: tuple[tuple[tuple[int, int, int, int], ...]]):
        super().__init__(game, (0, 0), pos)
        self.game: 'Game' = game
        self.max_size: tuple[int, int] = max_size
        self.pixelart: tuple[tuple[tuple[int, int, int, int], ...]] = pixelart

        self.update_view()

    def update_view(self):
        pixel_size: float = min(self.max_size[0] / len(self.pixelart[0]), self.max_size[1] / len(self.pixelart[1]))
        self.image = Surface((pixel_size * len(self.pixelart[0]), pixel_size * len(self.pixelart)), SRCALPHA,
                             32).convert_alpha()
        for y in range(len(self.pixelart)):
            for x in range(len(self.pixelart[y])):
                pg.draw.rect(self.image, self.pixelart[y][x], pg.Rect(
                    pixel_size * x, pixel_size * y, ceil(pixel_size), ceil(pixel_size)
                ))

    def update(self):
        pass

    @staticmethod
    def get_pixelart_by_image(path: str) -> tuple[tuple[tuple[int, int, int, int], ...]]:
        image: Image = Image.open(path).convert('RGBA')
        pixel_rows = [
            tuple(list(image.getdata())[i * image.size[0]: (i + 1) * image.size[0]])
            for i in range(image.size[1])
        ]
        return tuple[tuple[tuple[int, int, int, int], ...]](tuple(tuple(row) for row in pixel_rows))
