from typing import TYPE_CHECKING

from src.modules import TrafficLightData
from src.state import State
import time

from src.sprites import TrafficLight, Container, Text, TextAlign

if TYPE_CHECKING:
    from src.game import Game


class Dashboard(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.traffic_lights_uuids: list[str] = []

    def boot(self):
        self.add_sprite('traffic_lights_id_container', Container(self.game, (0, 0), (400, 1080)))
        self.add_sprite('traffic_lights_id_text', Text(self.game, (10, 10), 'Список ID светофоров:', 18,
                                                       (255, 255, 255), align=TextAlign.LEFT))

    def _add_traffic_lights_ids(self, traffic_lights_data: list[TrafficLightData]):
        for i, data in enumerate(traffic_lights_data):
            self.add_sprite(f'traffic_light_{data.uuid}_uuid',
                            Text(self.game, (30, 50 + 30 * i), data.uuid,
                                 16, (255, 255, 255), align=TextAlign.LEFT))
            self.traffic_lights_uuids.append(data.uuid)

    def _add_traffic_lights_images(self, traffic_lights_data: list[TrafficLightData]):
        for i, data in enumerate(traffic_lights_data):
            traffic_light = TrafficLight(self.game, data.tfl_type, data.uuid)
            self.add_sprite(f'traffic_light_{data.uuid}',
                            Container(self.game, (410 + i * 100, 10), (106, 106), traffic_light.get_cover))

    def update(self):
        if time.time() - self.game.last_ping_time >= 1 and self.game.pinger.running:
            self.game.pinger.ping()
            for uuid in self.traffic_lights_uuids:
                self.remove_sprite(f'traffic_light_{uuid}')
                self.remove_sprite(f'traffic_light_{uuid}_uuid')

            self._add_traffic_lights_ids(self.game.pinger.traffic_lights_data)
            self._add_traffic_lights_images(self.game.pinger.traffic_lights_data)

            self.game.last_ping_time = time.time()

    def enter(self):
        self.game.pinger.running = True

    def exit(self):
        self.game.pinger.running = False
