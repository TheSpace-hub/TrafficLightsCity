from typing import TYPE_CHECKING
from math import pi
import pygame as pg

from src.state import State

from src.sprites import Text, TextAlign, Field

if TYPE_CHECKING:
    from src.game import Game


class TrafficLightTextureEditor(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)

    def boot(self):
        pass

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass
