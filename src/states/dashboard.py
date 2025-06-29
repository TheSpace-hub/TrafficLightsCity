from typing import TYPE_CHECKING
from src.state import State

from src.sprites import TrafficLight, Container, Text, TextAlign

if TYPE_CHECKING:
    from src.game import Game


class Dashboard(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.traffic_lights: list[TrafficLight] = [
            TrafficLight(self.game, 'moscow_1', 'basic'),
            TrafficLight(self.game, 'moscow_2', 'basic'),
            TrafficLight(self.game, 'moscow_3', 'arrow'),
            TrafficLight(self.game, 'moscow_4', 'arrow')
        ]

    def boot(self):
        self.add_sprite('traffic_lights_id_container', Container(self.game, (0, 0), (400, 1080)))
        self.add_sprite('traffic_lights_id_text', Text(self.game, (10, 10), 'Список ID светофоров:', 18,
                                                       (255, 255, 255), align=TextAlign.LEFT))
        self._add_traffic_lights_ids()

    def _add_traffic_lights_ids(self):
        for i in range(len(self.traffic_lights)):
            self.add_sprite(f'traffic_light_{i}_id',
                            Text(self.game, (30, 50 + 30 * i), self.traffic_lights[i].data.uuid,
                                 16, (255, 255, 255), align=TextAlign.LEFT))

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass
