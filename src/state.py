"""
Основная сцена
"""
from typing import TYPE_CHECKING, TypeVar, Optional
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from src.game import Game
    from src.sprite import Sprite

T = TypeVar('T', bound='Sprite')


class State(ABC):
    """
    Основной класс сцены
    """

    def __init__(self, game: 'Game'):
        self.game: 'Game' = game
        self.sprites: dict[str, 'Sprite'] = {}

    def get_sprite(self, uuid: str) -> Optional['Sprite']:
        """
        Добавление спрайта на сцену
        :param uuid: Уникальный идентификатор спрайта
        :return: Спрайт или ничего, если uuid указан не верно
        """
        if uuid in self.sprites:
            return self.sprites[uuid]
        return None

    def add_sprite(self, uuid: str, obj: T) -> T:
        self.sprites[uuid] = obj
        return obj

    @abstractmethod
    def boot(self):
        """
        Вызывается при регистрации сцены
        """

    @abstractmethod
    def update(self):
        """
        Вызывается каждый кадр
        """

    @abstractmethod
    def enter(self):
        """
        Вызывается при переключении на сцену
        """

    @abstractmethod
    def exit(self):
        """
        Вызывается при выходе из сцены
        """
