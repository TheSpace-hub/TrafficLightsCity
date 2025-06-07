from typing import TYPE_CHECKING

from src.state import State

from src.sprites import Text

if TYPE_CHECKING:
    from src.game import Game


class Intro(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)

    def boot(self):
        self.add_sprite('text', Text(self.game, (400, 400), 'Test text', 32, (255, 255, 255)))

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass
