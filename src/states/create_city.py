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
                                            InBlockText(self.game, '', 16,
                                                        (255, 255, 255)),
                                            InBlockText(self.game, 'Введите seed...',
                                                        16, (128, 128, 128)),
                                            True
                                            ))
        self.add_sprite('create_city', Button(self.game, 510, 540, 900, 70,
                                              InBlockText(self.game, 'Создать новый город',
                                                          16, (255, 255, 255))
                                              ))

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass
