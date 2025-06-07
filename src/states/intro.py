import logging
from typing import TYPE_CHECKING
from enum import Enum

from src.state import State

from src.sprites import Text

if TYPE_CHECKING:
    from src.game import Game


class DirectionOfDecreasing(Enum):
    INCREASE = 3
    DECREASE = -3


class Intro(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.direction_of_decreasing_the_hint: DirectionOfDecreasing = DirectionOfDecreasing.DECREASE

    def boot(self):
        self.add_sprite('name',
                        Text(self.game, (960, 540), 'Город светофоров',
                             48, (255, 255, 255)))
        self.add_sprite('tip',
                        Text(self.game, (960, 600), 'Нажмите любую клавишу чтобы продолжить',
                             18, (200, 200, 200)))

    def update(self):
        tip: Text = self.get_sprite('tip')

        color: tuple[int, int, int] = tuple[int, int, int](
            tuple(map(lambda c: min(c + self.direction_of_decreasing_the_hint.value, 255), tip.color)))

        if tip.color[0] <= 100 and self.direction_of_decreasing_the_hint == DirectionOfDecreasing.DECREASE:
            self.direction_of_decreasing_the_hint = DirectionOfDecreasing.INCREASE
        elif tip.color[0] >= 200 and self.direction_of_decreasing_the_hint == DirectionOfDecreasing.INCREASE:
            self.direction_of_decreasing_the_hint = DirectionOfDecreasing.DECREASE

        tip.color = color
        tip.update_view()

    def enter(self):
        pass

    def exit(self):
        pass
