from typing import TYPE_CHECKING

from src.state import State

from src.sprites import Button, InBlockText, ButtonStatus, ChoiceOfSeveralOptions, Option

if TYPE_CHECKING:
    from src.game import Game


class Settings(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)

    def boot(self):
        self.add_sprite('back', Button(self.game, 1710, 1000, 200, 70,
                                       InBlockText(self.game, 'Назад', 16,
                                                   (255, 255, 255)),
                                       self.on_back_button_pressed))

        options: list[Option] = [
            Option(InBlockText(self.game, 'Test option 1', 16, (255, 255, 255)), 'Test1'),
            Option(InBlockText(self.game, 'Test option 2', 16, (255, 255, 255)), 'Test2'),
            Option(InBlockText(self.game, 'Test option 3', 16, (255, 255, 255)), 'Test3'),
        ]
        self.add_sprite('graphics_quality', ChoiceOfSeveralOptions(self.game, (100, 100), (500, 70),
                                                                   options))

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def on_back_button_pressed(self, status: ButtonStatus):
        if status == ButtonStatus.PRESSED:
            self.game.change_state('Menu')
