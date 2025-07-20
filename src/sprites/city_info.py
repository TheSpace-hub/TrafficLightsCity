from typing import TYPE_CHECKING
import pygame as pg
from pygame import SRCALPHA

from src.sprites import Text, TextAlign
from src.sprite import Sprite

if TYPE_CHECKING:
    from src.game import Game


class CityInfo(Sprite):
    """Класс для отображения информации о городе.
    """

    def __init__(self, game: 'Game', city_name: str, deaths: int = 0):
        super().__init__(game, (400, 800), (10, 10))
        self.game: 'Game' = game
        self.city_name: str = city_name
        self.deaths: int = 0

        self.update_view()

    def update_view(self):
        self.image.fill((32, 32, 32))
        pg.draw.rect(self.image, (78, 78, 78), pg.Rect(
            0, 0, self.image.get_size()[0], self.image.get_size()[1]
        ), 3)

        self.image.blit(Text(self.game, (0, 0), f'Город: {self.city_name}', 16,
                             (255, 255, 255), align=TextAlign.LEFT).image, (10, 10))

    def update(self):
        pass
