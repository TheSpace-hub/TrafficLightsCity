from typing import TYPE_CHECKING
from src.state import State

if TYPE_CHECKING:
    from src.game import Game


class Dashboard(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)

    def boot(self):
        pass

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass
