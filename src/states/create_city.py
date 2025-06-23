from typing import TYPE_CHECKING

from src.state import State

from src.sprites import Button, InBlockText, Input, ButtonStatus, ChoiceOfSeveralOptions, Option, Formatting

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
                                            Formatting.ONLY_DIGITS, 10
                                            ))
        field_sizes: list[Option] = [
            Option(InBlockText(self.game, 'Размер карты: Небольшой', 16, (255, 255, 255)), value='small'),
            Option(InBlockText(self.game, 'Размер карты: Средний', 16, (255, 255, 255)), value='medium'),
            Option(InBlockText(self.game, 'Размер карты: Большой', 16, (255, 255, 255)), value='large'),
        ]
        self.add_sprite('field_size', ChoiceOfSeveralOptions(self.game, (510, 540), (900, 70),
                                                             field_sizes))
        self.add_sprite('create_city', Button(self.game, 510, 620, 900, 70,
                                              InBlockText(self.game, 'Создать новый город',
                                                          16, (255, 255, 255)),
                                              self.on_create_city_button_pressed
                                              ))

        self.add_sprite('back', Button(self.game, 1710, 1000, 200, 70,
                                       InBlockText(self.game, 'Назад', 16,
                                                   (255, 255, 255)),
                                       self.on_back_button_pressed))

    def on_create_city_button_pressed(self, status: ButtonStatus):
        if status == ButtonStatus.PRESSED:
            seed_input: Input = self.get_sprite('seed_input')
            field_size: ChoiceOfSeveralOptions = self.get_sprite('field_size')

            context: dict = {
                'seed': None,
                'field_size': field_size.options[field_size.current_option].value
            }
            if seed_input.text.text.isdigit():
                context['seed'] = int(seed_input.text.text)
            self.game.change_state('City', context)

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def on_back_button_pressed(self, status: ButtonStatus):
        if status == ButtonStatus.PRESSED:
            self.game.change_state('Menu')
