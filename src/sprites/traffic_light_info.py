from typing import TYPE_CHECKING

from src.sprites import Container

if TYPE_CHECKING:
    from src.game import Game
    from src.modules import TrafficLightData


class TrafficLightInfo(Container):
    """Класс для отображения подробной информации о светофоре.
    """

    def __init__(self, game: 'Game', data: 'TrafficLightData'):
        super().__init__(game, (300, 800), (30, 30))
        self.game: 'Game' = game
        self.data: 'TrafficLightData' = data

        self.update_view()

    def update_view(self):
        super().update_view()

    def update(self):
        pass
