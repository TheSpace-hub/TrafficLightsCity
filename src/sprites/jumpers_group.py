from typing import TYPE_CHECKING
import pygame as pg
from pygame import SRCALPHA

from src.sprites import Jumper

from src.sprite import Sprite

if TYPE_CHECKING:
    from src.game import Game


class JumpersGroup(Sprite):
    def __init__(self, game: 'Game'):
        super().__init__(game, (1920, 1080))
        self.jumpers: list[Jumper] = []

    def update_view(self):
        self.image = pg.Surface((1920, 1080), SRCALPHA, 32).convert_alpha()
        for jumper in self.jumpers:
            jumper.update_view()
            self.image.blit(jumper.image, jumper.rect)

    def update(self):
        if len(self.jumpers) > 0:
            for jumper in self.jumpers:
                jumper.update()
            self.update_view()
