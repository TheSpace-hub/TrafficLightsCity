from typing import TYPE_CHECKING, Optional

from src.sprites import Container

if TYPE_CHECKING:
    from src.game import Game
    from src.modules import TrafficLightData


class TrafficLightInfo(Container):
    """Класс для отображения подробной информации о светофоре.
    """

    def __init__(self, game: 'Game'):
        super().__init__(game, (300, 800), (30, 30))
        self.game: 'Game' = game
        self.data: Optional['TrafficLightData'] = None

        self.update_view()

    def update_view(self):
        super().update_view()

    def show_data(self, data: 'TrafficLightData'):
        """Отобразить данные о светофоре.

        Args:
            data: Данные о светофоре.
        """
        self.data = data
        self.update_view()

    def close(self):
        """Закрыть информацию о текущем светофоре.
        """
        self.data = None
        self.update_view()

    def update(self):
        pass
