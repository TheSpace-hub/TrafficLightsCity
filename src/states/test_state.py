from typing import TYPE_CHECKING

import logging

from src.state import State

if TYPE_CHECKING:
    from src.game import Game


class TestState(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)

    def boot(self):
        logging.info('Test boot')

    def update(self):
        logging.info('Test update')

    def enter(self):
        logging.info('Test enter')

    def exit(self):
        logging.info('Test exit')
