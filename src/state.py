"""Модуль для работы с игровыми состояниями (сценами).

Содержит базовый абстрактный класс State, который:
- Определяет интерфейс для всех игровых сцен
- Управляет коллекцией спрайтов сцены
- Обеспечивает жизненный цикл сцены (инициализация, обновление, переход)
"""
from typing import TYPE_CHECKING, TypeVar, Optional
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from src.game import Game
    from src.sprite import Sprite

SpriteT = TypeVar('SpriteT', bound='Sprite')


class State(ABC):
    """Абстрактный базовый класс для всех игровых состояний (сцен).

    Предоставляет:
    - Управление коллекцией спрайтов сцены
    - Стандартизированный жизненный цикл сцены
    - Интеграцию с основным игровым объектом

    Attributes:
        game (Game): Ссылка на основной игровой объект
        sprites (dict[str, Sprite]): Словарь спрайтов сцены, где:
            ключ - уникальный идентификатор (uuid)
            значение - объект спрайта
    """

    def __init__(self, game: 'Game'):
        """Инициализирует состояние.

        Args:
            game: Ссылка на основной игровой объект
        """
        self.game: 'Game' = game
        self.sprites: dict[str, 'Sprite'] = {}

    def get_sprite(self, uuid: str) -> Optional[SpriteT]:
        """Возвращает спрайт по его уникальному идентификатору.

        Args:
            uuid: Уникальный идентификатор спрайта

        Returns:
            Найденный спрайт или None, если спрайт не существует
        """
        if uuid in self.sprites:
            return self.sprites[uuid]
        return None

    def get_sprites(self) -> dict[str, SpriteT]:
        """Возвращает все спрайты сцены.

        Returns:
            Словарь всех спрайтов в формате {uuid: sprite}
        """
        return self.sprites

    def remove_sprite(self, uuid):
        """Удаляет спрайт из сцены.

        Args:
            uuid: Уникальный идентификатор спрайта для удаления

        Note:
            Не вызывает ошибку, если спрайт не существует
        """
        if uuid in self.sprites:
            del self.sprites[uuid]

    def add_sprite(self, uuid: str, obj: SpriteT) -> SpriteT:
        """Добавляет новый спрайт на сцену.

        Args:
            uuid: Уникальный идентификатор для нового спрайта
            obj: Объект спрайта для добавления

        Returns:
            Добавленный спрайт (тот же, что и в параметре obj)

        Raises:
            ValueError: Если спрайт с таким uuid уже существует
        """
        self.sprites[uuid] = obj
        return obj

    @abstractmethod
    def boot(self):
        """Инициализация сцены при регистрации.

        Вызывается один раз при регистрации сцены в Game.
        """

    @abstractmethod
    def update(self):
        """Обновляет логику сцены.

        Вызывается каждый игровой кадр.
        """

    @abstractmethod
    def enter(self):
        """Обработчик входа в сцену.

        Вызывается при переключении на эту сцену.
        """

    @abstractmethod
    def exit(self):
        """Обработчик выхода из сцены.

        Вызывается при переключении на другую сцену.
        """
