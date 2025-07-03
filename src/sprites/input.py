from typing import TYPE_CHECKING
from enum import Enum

import pygame as pg

from src.sprites import InBlockText

from src.sprite import Sprite

if TYPE_CHECKING:
    from src.game import Game


class InputStatus(Enum):
    NONE = 0
    SELECTED = 1


class Formatting(Enum):
    NO_FORMATTING = 0
    ONLY_DIGITS = 1
    NORMALIZED = 2


class Input(Sprite):
    def __init__(self, game: 'Game', pos: tuple[int, int], size: tuple[int, int], text: InBlockText,
                 placeholder: InBlockText, formatting: Formatting = Formatting.NO_FORMATTING, limit: int = 0,
                 enabled: bool = True):
        super().__init__(game, size, pos)
        self.text: InBlockText = text
        self.placeholder: InBlockText = placeholder
        self.status: InputStatus = InputStatus.NONE
        self.limit: int = limit
        self.formatting: Formatting = formatting
        self.enabled: bool = enabled

        text.correct_position(size)
        placeholder.correct_position(size)

        self.update_view()

    def update_view(self):
        if self.status == InputStatus.SELECTED or not self.enabled:
            self.image.fill((58, 58, 58))
        elif self.status == InputStatus.NONE:
            self.image.fill((32, 32, 32))

        if self.text.text == '':
            self.image.blit(self.placeholder.image, self.placeholder.rect)
        else:
            self.image.blit(self.text.image, self.text.rect)
        pg.draw.rect(self.image, (78, 78, 78), pg.Rect(
            0, 0, self.image.get_size()[0], self.image.get_size()[1]
        ), 3)

    def update(self):
        if pg.mouse.get_pressed()[0]:
            if (self.rect.x < pg.mouse.get_pos()[0] < self.rect.x + self.image.get_size()[0] and self.rect.y <
                    pg.mouse.get_pos()[1]
                    < self.rect.y + self.image.get_size()[1] and self.enabled):
                self.status = InputStatus.SELECTED
                self.update_view()
            else:
                self.status = InputStatus.NONE
                self.update_view()
        if self.status != InputStatus.SELECTED:
            return

        for key in self.game.omitted_buttons:
            if 32 <= key <= 126 and self.enabled and (len(self.text.text) < self.limit or self.limit <= 0):
                if self.formatting == Formatting.ONLY_DIGITS and not (48 <= key <= 57):
                    continue
                if self.formatting == Formatting.NORMALIZED and not (97 <= key <= 122 or 48 <= key <= 57):
                    if key == 32:
                        key = 95
                    else:
                        continue
                self.text.text += chr(key)
                self.text.correct_position((self.image.get_size()[0], self.image.get_size()[1]))
                self.text.update_view()
                self.update_view()
            if key == 8:
                self.text.text = self.text.text[:-1]
                self.text.correct_position((self.image.get_size()[0], self.image.get_size()[1]))
                self.text.update_view()
                self.update_view()
