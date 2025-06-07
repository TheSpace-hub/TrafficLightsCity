from typing import TYPE_CHECKING
from enum import Enum

from src.state import State

from src.sprites import Text

if TYPE_CHECKING:
    from src.game import Game



class Menu(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)

    def boot(self):
        self.add_sprite('name', Text(self.game, (960, 540), 'Меню',
                             48, (255, 255, 255)))

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass
