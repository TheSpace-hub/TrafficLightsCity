"""Модуль создания города.
"""
from typing import TYPE_CHECKING
from random import choice
from os import path, listdir

from src.state import State

from src.sprites import Button, InBlockText, Input, ButtonStatus, ChoiceOfSeveralOptions, Option, Formatting

if TYPE_CHECKING:
    from src.game import Game


class CreateCity(State):
    """Класс сцены с настройками создания города.
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
        self.add_sprite('seed_input', Input(self.game, (510, 460), (900, 70),
                                            InBlockText(self.game, '', 16,
                                                        (255, 255, 255)),
                                            InBlockText(self.game, 'Введите seed или оставьте пустым',
                                                        16, (128, 128, 128)),
                                            Formatting.ONLY_DIGITS, 10
                                            ))
        field_sizes: list[Option] = [
            Option(InBlockText(self.game, 'Размер карты: Небольшой', 16, (255, 255, 255)), value='small'),
            Option(InBlockText(self.game, 'Размер карты: Средний', 16, (255, 255, 255)), value='medium'),
            Option(InBlockText(self.game, 'Размер карты: Большой', 16, (255, 255, 255)), value='large'),
        ]
        self.add_sprite('field_size', ChoiceOfSeveralOptions(self.game, (510, 540), (900, 70),
                                                             field_sizes))
        self.add_sprite('create_city', Button(self.game, (510, 620), (900, 70),
                                              InBlockText(self.game, 'Создать новый город',
                                                          16, (255, 255, 255)),
                                              self.on_create_city_button_pressed
                                              ))

        self.add_sprite('back', Button(self.game, (1710, 1000), (200, 70),
                                       InBlockText(self.game, 'Назад', 16,
                                                   (255, 255, 255)),
                                       self.on_back_button_pressed))

    def on_create_city_button_pressed(self, status: ButtonStatus):
        """Действие при нажатии на кнопку создания города.

        Переключается на сцену "City" и передаёт введённые данные.
        """
        if status == ButtonStatus.PRESSED:
            seed_input: Input = self.get_sprite('seed_input')
            field_size: ChoiceOfSeveralOptions = self.get_sprite('field_size')

            field_sizes: dict[str, tuple[int, int]] = {
                'small': (30, 30),
                'medium': (50, 50),
                'large': (80, 80)
            }

            context: dict = {
                'name': self.generate_uuid_for_city(),
                'deaths': 0,
                'seed': None,
                'size': field_sizes[field_size.options[field_size.current_option].value],
                'traffic_lights': []
            }
            if seed_input.text.text.isdigit():
                context['seed'] = int(seed_input.text.text)
            self.game.change_state('City', context)

    @staticmethod
    def generate_uuid_for_city() -> str:
        """Создание уникального названия для города.
        """
        cities: list[str] = [
            "moscow", "saintpetersburg", "novosibirsk", "yekaterinburg", "kazan",
            "nizhnynovgorod", "chelyabinsk", "samara", "omsk", "rostovondon",
            "ufa", "krasnoyarsk", "perm", "voronezh", "volgograd", "krasnodar",
            "saratov", "tyumen", "tolyatti", "izhevsk", "barnaul", "ulyanovsk",
            "irkutsk", "khabarovsk", "yaroslavl", "vladivostok", "makhachkala",
            "tomsk", "orenburg", "kemerovo", "novokuznetsk", "ryazan", "astrakhan",
            "naberezhnyechelny", "penza", "lipetsk", "kirov", "cheboksary",
            "tula", "kaliningrad", "balashikha", "kursk", "stavropol", "sochi",
            "ivanovo", "tver", "bryansk", "belgorod", "arzamas", "vladimir",
            "chita", "grozny", "kaluga", "smolensk", "volzhsky", "murmansks",
            "vladikavkaz", "saransk", "yakutsk", "sterlitamak", "orsk", "severodvinsk",
            "novorossiysk", "nizhnekamsk", "shakhty", "dzerzhinsk", "engels",
            "biysk", "prokopyevsk", "rybinsk", "balakovo", "armavir", "lobnya",
            "seversk", "mezhdurechensk", "kamenskuralsky", "miass", "elektrostal",
            "zlatoust", "serpukhov", "kopeyk", "almetyevsk", "odintsovo", "korolyov",
            "lyubertsy", "kovrov", "novouralsk", "khasavyurt", "pyatigorsk",
            "serov", "arzamas", "berezniki", "kislovodsk", "anapa", "gelendzhik",
            "yeysk", "komsomolsknaamure", "nizhnevartovsk", "novyurengoy",
            "magadan", "norilsk", "salekhard", "surgut", "khanty-mansiysk",
            "yuzhnosakhalinsk", "vorkuta", "nadym", "gubkinsky", "murmansk",
            "severomorsk", "arzamas", "arzamas", "ivanteevka"
        ]
        uuid = choice(cities)
        while f'{uuid}.json' in [file for file in listdir(path.join('saves', 'cities')) if file.endswith('.json')]:
            uuid = choice(cities)

        return uuid

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
