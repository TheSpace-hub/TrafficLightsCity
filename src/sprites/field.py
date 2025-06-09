from typing import TYPE_CHECKING
from math import sin, cos, sqrt, radians

from src.sprite import Sprite
from src.sprites import Tile, TileTexture

if TYPE_CHECKING:
    from src.game import Game


class Field(Sprite):
    """
    Поле. Состоит из объектов типа Tile
    """

    def __init__(self, game: 'Game'):
        self._perspective_angle = 30
        super().__init__(game, (1920, 1080), (0, 0))
        self.tile_size = 10
        self.pixel_size = 10

        self.update_view()

    def update_view(self):
        for i in range(10):
            tile = Tile(self.game, 10, 10, TileTexture.GRASS)
            self.image.blit(tile.image,
                            (i * int(self.tile_size * self.pixel_size * cos(radians(self._perspective_angle))),
                             int(i * self.tile_size * self.pixel_size * sin(radians(self._perspective_angle)))))

    def update(self):
        pass
