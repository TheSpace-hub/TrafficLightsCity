from typing import TYPE_CHECKING

from src.state import State

from src.sprites import Text, TextAlign

if TYPE_CHECKING:
    from src.game import Game


class City(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)

    def boot(self):
        self.add_sprite('city_name', Text(self.game, (0, 0), 'City.01', 16,
                                          (255, 255, 255), align=TextAlign.LEFT))

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass
