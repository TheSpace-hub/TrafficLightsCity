from typing import TYPE_CHECKING
import pygame as pg

from src.sprites import InBlockText, Button, ButtonStatus

from src.sprite import Sprite

if TYPE_CHECKING:
    from src.game import Game


class Option:
    def __init__(self, text: InBlockText, value: str, enabled: bool = True):
        self.text: InBlockText = text
        self.value: str = value
        self.enabled: bool = enabled


class ChoiceOfSeveralOptions(Sprite):
    def __init__(self, game: 'Game', pos: tuple[int, int], size: tuple[int, int], options: list[Option],
                 enabled: bool = True):
        super().__init__(game, size, pos)
        self.options: list[Option] = options
        self.current_option: int = 0
        self.enabled: bool = enabled

        self.button_previous: Button = Button(self.game, 0, 0, self.image.get_size()[1], self.image.get_size()[1],
                                              InBlockText(self.game, '<', 16, (255, 255, 255)),
                                              self.on_previous_button_pressed, offset=pos)
        self.button_next: Button = Button(self.game, self.image.get_size()[0] - self.image.get_size()[1], 0,
                                          self.image.get_size()[1], self.image.get_size()[1],
                                          InBlockText(self.game, '>', 16, (255, 255, 255)),
                                          self.on_next_button_pressed, offset=pos)

        for option in self.options:
            option.text.correct_position(size)

    def update_view(self):
        self.image.fill((32, 32, 32))
        self.image.blit(self.button_previous.image, self.button_previous.rect)
        self.image.blit(self.button_next.image, self.button_next.rect)

        option: Option = self.options[self.current_option]
        self.image.blit(option.text.image, option.text.rect)
        pg.draw.rect(self.image, (78, 78, 78), pg.Rect(0, 0, self.image.get_size()[0], self.image.get_size()[1]), 3)

    def update(self):
        self.button_previous.update()
        self.button_next.update()
        self.update_view()

    def on_previous_button_pressed(self, status: ButtonStatus):
        if status == ButtonStatus.PRESSED:
            self.current_option = len(self.options) - 1 if self.current_option == 0 else self.current_option - 1

    def on_next_button_pressed(self, status: ButtonStatus):
        if status == ButtonStatus.PRESSED:
            self.current_option = 0 if self.current_option == len(self.options) - 1 else self.current_option + 1
