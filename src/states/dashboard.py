from typing import TYPE_CHECKING
from src.state import State

from src.sprites import TrafficLight, Container, Text, TextAlign

if TYPE_CHECKING:
    from src.game import Game


class Dashboard(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.traffic_lights: list[TrafficLight] = [
            TrafficLight(self.game, 'basic', 'moscow_1'),
            TrafficLight(self.game, 'arrow', 'moscow_2'),
            TrafficLight(self.game, 'basic', 'moscow_3'),
            TrafficLight(self.game, 'arrow', 'moscow_4'),
        ]

    def boot(self):
        self.add_sprite('traffic_lights_id_container', Container(self.game, (0, 0), (400, 1080)))
        self.add_sprite('traffic_lights_id_text', Text(self.game, (10, 10), 'Список ID светофоров:', 18,
                                                       (255, 255, 255), align=TextAlign.LEFT))
        self._add_traffic_lights_ids()
        self._add_traffic_lights_images()

    def _add_traffic_lights_ids(self):
        for i in range(len(self.traffic_lights)):
            traffic_light = self.traffic_lights[i]
            self.add_sprite(f'traffic_light_{traffic_light.data.uuid}_uuid',
                            Text(self.game, (30, 50 + 30 * i), self.traffic_lights[i].data.uuid,
                                 16, (255, 255, 255), align=TextAlign.LEFT))

    def _add_traffic_lights_images(self):
        for i in range(len(self.traffic_lights)):
            traffic_light = self.traffic_lights[i]
            self.add_sprite(f'traffic_light_{traffic_light.data.uuid}',
                            Container(self.game, (410 + i * 100, 10), (106, 106), traffic_light.get_cover))

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass
