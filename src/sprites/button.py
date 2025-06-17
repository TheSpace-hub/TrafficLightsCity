from typing import TYPE_CHECKING, Callable
import os
from enum import Enum

import pygame as pg

from src.sprites.text import Text

from src.sprite import Sprite

if TYPE_CHECKING:
    from src.game import Game


class ButtonStatus(Enum):
    NONE = 0
    HOLD = 1
    PRESSED = 2
    HOVERED = 3


class ButtonView(Enum):
    NORMAL = 0
    HOVERED = 1
    PRESSED = 2


class InBlockText(Text):
    def __init__(self, game: 'Game', text: str, font_size: int,
                 color: tuple[int, int, int, int] | tuple[int, int, int],
                 font_path: str = os.path.join('assets', 'fonts', 'MainFont.ttf')):
        super().__init__(game, (0, 0), text, font_size, color, font_path)

    def correct_position(self, size: tuple[int, int]):
        self.rect.x = int(size[0] / 2) - int(self.image.get_size()[0] / 2)
        self.rect.y = int(size[1] / 2) - int(self.image.get_size()[1] / 2)

    def update_view(self):
        super().update_view()

    def update(self):
        super().update()


class Button(Sprite):
    def __init__(self, game: 'Game', x: int, y: int, size_x: int, size_y: int, text: InBlockText,
                 func: Callable[[ButtonStatus], None] = None, enabled: bool = True):
        super().__init__(game, (size_x, size_y), (x, y))
        self.text: InBlockText = text
        self.func: Callable[[ButtonStatus], None] = func
        self.last_status: ButtonStatus = ButtonStatus.NONE
        self.last_view: ButtonView = ButtonView.NORMAL
        self.view: ButtonView = ButtonView.NORMAL
        self.enabled: bool = enabled

        text.correct_position((size_x, size_y))

    def update_view(self):
        if self.view == ButtonView.PRESSED or not self.enabled:
            self.image.fill((58, 58, 58))
        elif self.view == ButtonView.HOVERED:
            self.image.fill((23, 23, 23))
        elif self.view == ButtonView.NORMAL:
            self.image.fill((32, 32, 32))
        self.image.blit(self.text.image, self.text.rect)
        pg.draw.rect(self.image, (78, 78, 78), pg.Rect(
            0, 0, self.image.get_size()[0], self.image.get_size()[1]
        ), 3)

    def update(self):
        if (self.rect.x < pg.mouse.get_pos()[0] < self.rect.x + self.image.get_size()[0] and self.rect.y <
                pg.mouse.get_pos()[1]
                < self.rect.y + self.image.get_size()[1] and self.enabled):
            if self.last_view != ButtonView.HOVERED or self.last_view != ButtonView.PRESSED:
                self.view = ButtonView.HOVERED
                self.update_view()
                if self.last_status == ButtonStatus.NONE:
                    self.last_status = ButtonStatus.HOVERED
            if pg.mouse.get_pressed()[0]:
                self.view = ButtonView.PRESSED
                self.update_view()
                if self.func is not None:
                    self.func(ButtonStatus.HOLD)
                self.last_status = ButtonStatus.HOLD
            elif self.last_status == ButtonStatus.HOLD:
                if self.func is not None:
                    self.func(ButtonStatus.PRESSED)
                self.last_status = ButtonStatus.NONE
        else:
            self.view = ButtonView.NORMAL
            self.update_view()
            self.last_status = ButtonStatus.NONE
