from typing import TYPE_CHECKING, Callable
import pygame as pg

from src.sprite import Sprite

if TYPE_CHECKING:
    from src.game import Game


class Container(Sprite):
    def __init__(self, game: 'Game', pos: tuple[int, int], size: tuple[int, int],
                 placeholder: Callable[[], pg.Surface] | None = None):
        super().__init__(game, size, pos)
        self.placeholder: Callable[[], pg.Surface] | None = placeholder
        self.update_view()

    def update_view(self):
        self.image.fill((32, 32, 32))
        pg.draw.rect(self.image, (78, 78, 78), pg.Rect(
            0, 0, self.image.get_size()[0], self.image.get_size()[1]
        ), 3)
        if self.placeholder is not None:
            placeholder: pg.Surface = self.placeholder()
            self.image.blit(placeholder, (3, 3))

    def update(self):
        pass
