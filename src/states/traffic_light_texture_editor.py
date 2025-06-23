from typing import TYPE_CHECKING

from src.state import State

from src.sprites import Pixelart

if TYPE_CHECKING:
    from src.game import Game


class TrafficLightTextureEditor(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)

    def boot(self):
        self.add_sprite('pixelatr1', Pixelart(self.game, (100, 100), 10, (((0, 0, 0),),)))

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass
