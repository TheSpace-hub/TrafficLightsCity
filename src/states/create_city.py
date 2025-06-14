from typing import TYPE_CHECKING

from src.state import State

from src.sprites import Button, InBlockText, Input, ButtonStatus

if TYPE_CHECKING:
    from src.game import Game


class CreateCity(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)

    def boot(self):
        self.add_sprite('seed_input', Input(self.game, 510, 460, 900, 70,
                                            InBlockText(self.game, '', 16,
                                                        (255, 255, 255)),
                                            InBlockText(self.game, 'Введите seed или оставьте пустым',
                                                        16, (128, 128, 128)),
                                            True, 10
                                            ))
        self.add_sprite('create_city', Button(self.game, 510, 540, 900, 70,
                                              InBlockText(self.game, 'Создать новый город',
                                                          16, (255, 255, 255)),
                                              self.on_create_city_button_pressed
                                              ))

    def on_create_city_button_pressed(self, status: ButtonStatus):
        if status == ButtonStatus.PRESSED:
            seed_input: Input = self.get_sprite('seed_input')
            if seed_input.text.text.isdigit():
                self.game.change_state('City', {'seed': int(seed_input.text.text)})
            else:
                self.game.change_state('City')

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass
