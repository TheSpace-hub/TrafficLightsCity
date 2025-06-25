from typing import TYPE_CHECKING
from src.state import State

from src.sprites import TrafficLight

if TYPE_CHECKING:
    from src.game import Game


class Dashboard(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)

    def boot(self):
        self.add_sprite('tfl', TrafficLight(self.game, 'arrow'))

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass
