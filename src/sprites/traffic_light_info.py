from typing import TYPE_CHECKING, Optional
import pygame as pg
from pygame import SRCALPHA

from src.sprite import Sprite

if TYPE_CHECKING:
    from src.game import Game
    from src.modules import TrafficLightData


class TrafficLightInfo(Sprite):
    """Класс для отображения подробной информации о светофоре.
    """

    def __init__(self, game: 'Game'):
        super().__init__(game, (400, 800), (1510, 10))
        self.game: 'Game' = game
        self.data: Optional['TrafficLightData'] = None

        self.update_view()

    def update_view(self):
        if self.data is None:
            self.image = pg.Surface(self.image.get_size(), SRCALPHA, 32).convert_alpha()
            return
        self.image.fill((32, 32, 32))
        pg.draw.rect(self.image, (78, 78, 78), pg.Rect(
            0, 0, self.image.get_size()[0], self.image.get_size()[1]
        ), 3)

    def update(self):
        pass
