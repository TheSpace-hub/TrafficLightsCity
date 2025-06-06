"""
Компонент отображаемый на сцене
"""

from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from pygame import Surface, sprite, Rect, SRCALPHA

if TYPE_CHECKING:
    from src.game import Game


class Sprite(sprite.Sprite, ABC):
    def __init__(self, game: 'Game', size: tuple[int, int], position: tuple[int, int] = (0, 0)):
        super().__init__()
        self.game: 'Game' = game
        self.image: Surface = Surface(size, SRCALPHA, 32).convert_alpha()
        self.rect: Rect = self.image.get_rect()
        self.rect.x, self.rect.y = position[0], position[1]

    @abstractmethod
    def update_view(self):
        """
        Обновить изображение
        Вызывается самостоятельно
        """
        self.image = Surface(self.image.get_size(), SRCALPHA, 32).convert_alpha()

    @abstractmethod
    def update(self):
        """
        Вызывается каждый кадр
        """
