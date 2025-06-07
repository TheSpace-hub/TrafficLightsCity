from typing import TYPE_CHECKING

from src.state import State

from src.sprites import Button, InBlockText, Input

if TYPE_CHECKING:
    from src.game import Game


class CreateCity(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)

    def boot(self):
        self.add_sprite('seed_input', Input(self.game, 510, 460, 900, 70,
                                            InBlockText(self.game, 'ЭТО ПОЛЕ ДЛЯ СИДА', 16,
                                                        (255, 255, 255)),
                                            ))
        # self.add_sprite('seed', Button(self.game, 510, 460, 900, 70,
        #                                InBlockText(self.game, 'ЭТО ПОЛЕ ДЛЯ СИДА', 16,
        #                                            (255, 255, 255)),
        #                                ))

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass
