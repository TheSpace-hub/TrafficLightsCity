from typing import TYPE_CHECKING, Callable
from math import ceil
import pygame as pg
from pygame import Surface, SRCALPHA
from PIL import Image

from src.sprites import Container

if TYPE_CHECKING:
    from src.game import Game


class Jumper(Container):
    def __init__(self, game: 'Game', pos: tuple[int, int], size: tuple[int, int],
                 placeholder: Callable[[], pg.Surface] | None = None):
        self.zoom: float = 0
        super().__init__(game, pos, size, placeholder)

    def update_view(self):
        self.image.fill((32, 32, 32))
        if self.placeholder is not None:
            placeholder: pg.Surface = self.placeholder()
            new_size = (
                placeholder.get_size()[0] * self.zoom ** 2,
                placeholder.get_size()[1] * self.zoom ** 2,
            )
            self.image.blit(
                pg.transform.scale(placeholder, new_size, None), (3, 3))
    def update(self):
        self.update_view()
        self.zoom += .01
