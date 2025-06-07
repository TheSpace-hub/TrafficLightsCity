from typing import TYPE_CHECKING

from src.state import State

from src.sprites import Text, Button, InButtonText

if TYPE_CHECKING:
    from src.game import Game



class Menu(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)

    def boot(self):
        self.add_sprite('settings', Button(self.game, 10, 10, 150, 150,
                                           InButtonText(self.game, 'Test', 16, (255, 255, 255))))

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass
