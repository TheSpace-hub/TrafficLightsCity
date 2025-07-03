from typing import TYPE_CHECKING
from os import path
import json
from src.state import State

from src.sprites import Button, InBlockText, ButtonStatus, ChoiceOfSeveralOptions, Option

if TYPE_CHECKING:
    from src.game import Game


class Settings(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)

    def boot(self):
        self.add_sprite('back', Button(self.game, (1710, 1000), (200, 70),
                                       InBlockText(self.game, 'Назад', 16,
                                                   (255, 255, 255)),
                                       self.on_back_button_pressed))

        options: list[Option] = [
            Option(InBlockText(self.game, 'Качество: Низкое', 16, (255, 255, 255)), 'low'),
            Option(InBlockText(self.game, 'Качество: Среднее', 16, (255, 255, 255)), 'medium'),
            Option(InBlockText(self.game, 'Качество: Высокое', 16, (255, 255, 255)), 'high'),
        ]
        self.add_sprite('graphics_quality', ChoiceOfSeveralOptions(self.game, (710, 460), (500, 70),
                                                                   options, self.on_graphics_quality_changed))

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def on_back_button_pressed(self, status: ButtonStatus):
        if status == ButtonStatus.PRESSED:
            self.game.change_state('Menu')

    @staticmethod
    def on_graphics_quality_changed(value: str):
        settings: dict = {
            'version': 0.1,
            'graphic': {
                'graphics_quality': value
            }
        }
        with open(path.join('saves', 'settings.json'), 'w') as f:
            f.write(json.dumps(settings))
