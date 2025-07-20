from typing import TYPE_CHECKING
import pygame as pg
from pygame import SRCALPHA
from math import sqrt

from src.sprite import Sprite

if TYPE_CHECKING:
    from src.game import Game
    from src.sprites import Jumper


class JumpersGroup(Sprite):
    def __init__(self, game: 'Game'):
        super().__init__(game, (1920, 1080))
        self.jumpers: list['Jumper'] = []

    def update_view(self):
        self.image = pg.Surface((1920, 1080), SRCALPHA, 32).convert_alpha()
        for jumper in self.jumpers:
            jumper.update_view()
            self.image.blit(jumper.image, jumper.rect)

    def add_jumper(self, jumper: 'Jumper'):
        self.jumpers.append(jumper)

    def update(self):
        if len(self.jumpers) > 0:
            self.jumpers = list(filter(
                lambda j: j.index < sqrt(2),
                self.jumpers
            ))
            for jumper in self.jumpers:
                jumper.update()
            self.update_view()
