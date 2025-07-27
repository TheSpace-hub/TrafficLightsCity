"""Модуль открытия города.
"""
from typing import TYPE_CHECKING
from os import path, listdir

from src.state import State

from src.sprites import Button, InBlockText, ButtonStatus, ChoiceOfSeveralOptions, Text, TextAlign, Option

if TYPE_CHECKING:
    from src.game import Game


class OpenCity(State):
    """Класс сцены выбором города.
    """

    def __init__(self, game: 'Game'):
        """Создание сцены.

        Args:
            game (Game): Экземпляр игры
        """
        super().__init__(game)

    def boot(self):
        """Инициализация сцены.
        """
        self.add_sprite('header_text', Text(self.game, (960, 500), 'Выберите город:',
                                            24, (255, 255, 255)))

        self.create_open_city_choice()

        self.add_sprite('back', Button(self.game, (1710, 1000), (200, 70),
                                       InBlockText(self.game, 'Назад', 16,
                                                   (255, 255, 255)),
                                       self.on_back_button_pressed))

    def create_open_city_choice(self):
        """Создание строки для выбора города.
        """
        cities: list[str] = [file for file in listdir(path.join('saves', 'maps')) if file.endswith('.json')]
        options: list[Option] = []
        for city in cities:
            options.append(
                Option(InBlockText(self.game, city, 16, (255, 255, 255)), f'city_{city}')
            )

        if not options:
            options = [Option(InBlockText(self.game, 'Ни одного города не существует', 16, (128, 128, 128)), 'null')]

        self.add_sprite('choice_city', ChoiceOfSeveralOptions(self.game, (510, 540), (900, 70),
                                                              options))

    def on_open_city_button_pressed(self, status: ButtonStatus, context: str):
        """Действие при нажатии на одну из кнопок для открытия города.
        """

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def on_back_button_pressed(self, status: ButtonStatus):
        """Переход обратно в меню.
        """
        if status == ButtonStatus.PRESSED:
            self.game.change_state('Menu')
