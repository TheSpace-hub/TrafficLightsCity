from typing import TYPE_CHECKING

from src.state import State

from src.sprites import Text, TextAlign, Tile, TileTexture

if TYPE_CHECKING:
    from src.game import Game


class City(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)

    def boot(self):
        self.add_sprite('city_name', Text(self.game, (10, 10), 'City.01', 16,
                                          (255, 255, 255), align=TextAlign.LEFT))

        self.add_sprite('test_tile', Tile(self.game, 300, 300, 10, 10, 10,
                                          TileTexture.GRASS))

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass
