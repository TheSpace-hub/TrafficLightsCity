"""Модуль для работы с базовыми спрайтами игры.

Содержит абстрактный класс Sprite, который:
- Предоставляет базовую функциональность для всех игровых спрайтов
- Обеспечивает стандартный интерфейс для обновления и отрисовки
- Интегрируется с системой pygame.sprite

Основные возможности:
- Автоматическая работа с поверхностями (Surface)
- Поддержка прозрачности (SRCALPHA)
- Абстрактные методы для обязательной реализации
"""

from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from pygame import Surface, sprite, Rect, SRCALPHA

if TYPE_CHECKING:
    from src.game import Game


class Sprite(sprite.Sprite, ABC):
    """Абстрактный базовый класс для всех игровых спрайтов.

        Наследует функциональность pygame.sprite.Sprite и добавляет:
        - Интеграцию с игровым движком (через ссылку на Game)
        - Поддержку прозрачности
        - Стандартизированный интерфейс обновления

        Attributes:
            game (Game): Ссылка на основной игровой объект
            image (Surface): Графическое представление спрайта
            rect (Rect): Прямоугольник, определяющий позицию и размер

        Note:
            Все наследники должны реализовать абстрактные методы:
            - update_view()
            - update()
        """

    def __init__(self, game: 'Game', size: tuple[int, int], position: tuple[int, int] = (0, 0)):
        """Инициализирует спрайт.

        Args:
            game: Ссылка на основной игровой объект
            size: Размер спрайта в пикселях (ширина, высота)
            position: Начальная позиция спрайта (x, y). По умолчанию (0, 0)
        """
        super().__init__()
        self.game: 'Game' = game
        self.image: Surface = Surface(size, SRCALPHA, 32).convert_alpha()
        self.rect: Rect = self.image.get_rect()
        self.rect.x, self.rect.y = position[0], position[1]

    @abstractmethod
    def update_view(self):
        """Обновляет графическое представление спрайта.

        Должен быть реализован в дочерних классах.
        Вызывается при необходимости перерисовки спрайта.

        Note:
            - Должен модифицировать self.image
            - По умолчанию просто создает новую прозрачную поверхность
            - Для оптимизации следует избегать частых вызовов
        """
        self.image = Surface(self.image.get_size(), SRCALPHA, 32).convert_alpha()

    @abstractmethod
    def update(self):
        """Обновляет логику спрайта.

        Должен быть реализован в дочерних классах.
        Вызывается каждый игровой кадр.

        Note:
            - Сюда помещается основная логика поведения спрайта
            - Не должен содержать тяжелых вычислений
            - Для графических изменений используйте update_view()
        """
