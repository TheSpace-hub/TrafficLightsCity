from typing import TYPE_CHECKING

from src.sprites import Pixelart
from src.sprite import Sprite

if TYPE_CHECKING:
    from src.game import Game


class Jumper(Sprite):
    def __init__(self, game: 'Game', pos: tuple[int, int],
                 pixelart: tuple[tuple[tuple[int, int, int, int], ...]]):
        super().__init__(game, (30, 30), pos)
        self.pixelart: tuple[tuple[tuple[int, int, int, int], ...]] = pixelart

    def update_view(self):
        self.image = Pixelart(self.game, (0, 0), (30, 30), self.pixelart).image

    def update(self):
        self.update_view()
