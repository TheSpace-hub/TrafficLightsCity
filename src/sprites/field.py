from typing import TYPE_CHECKING

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
        self.update_view()

    def update_view(self):
        tile_1 = Tile(self.game, 10, 10, TileTexture.GRASS)
        self.image.blit(tile_1.image, (10, 10))

    def update(self):
        pass
