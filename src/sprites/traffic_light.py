import json
from typing import TYPE_CHECKING
from os import path

from src.sprite import Sprite

if TYPE_CHECKING:
    from src.game import Game


class TrafficLightSegment:
    def __init__(self, pos: tuple[int, int], texture: str):
        self.pos: tuple[int, int] = pos
        self.texture: str = texture


class TrafficLightData:
    def __init__(self, tfl_type: str):
        self.tfl_type: str = tfl_type
        data: dict = self.get_traffic_light_data()

        self.url: str = data['url']
        self.type_use: bool = self.get_type_use(data)
        self.type_value: str = self.get_type_value(data)
        self.segments: dict[str, TrafficLightSegment] = self.get_segments(data)
        self.states: list[dict[str, str]] = self.get_states(data)

    def get_traffic_light_data(self) -> dict:
        with open(path.join('saves', 'traffic_lights', f'{self.tfl_type}.json'), 'r') as file:
            return json.loads(file.read())

    @staticmethod
    def get_url(data: dict) -> str:
        return str(data['url'])

    @staticmethod
    def get_type_use(data: dict) -> bool:
        return bool(data['type']['use'])

    @staticmethod
    def get_type_value(data: dict) -> str:
        return str(data['type']['value'])

    @staticmethod
    def get_segments(data: dict) -> dict[str, TrafficLightSegment]:
        segments: dict[str, TrafficLightSegment] = {}
        for name, segment in data['segments'].items():
            segments[name] = TrafficLightSegment(
                (int(segment['pos']['x']), int(segment['pos']['y'])),
                str(segment['texture'])
            )
        return segments

    @staticmethod
    def get_states(data: dict) -> list[dict[str, str]]:
        states: list[dict[str, str]] = []
        for state in data['states']:
            states.append(state)
        return states

    def __str__(self):
        return (f'"url": {self.url},'
                f'"type":'
                f'  "use": {self.type_use},'
                f'  "value": {self.type_value}'
                f'"segments": {self.segments},'
                f'"states": {self.states}')


class TrafficLight(Sprite):
    def __init__(self, game: 'Game', tfl_type: str):
        super().__init__(game, (0, 0), (0, 0))
        self.game: 'Game' = game
        self.data = TrafficLightData(tfl_type)
        print(self.data)

        self.update_view()

    def update_view(self):
        pass

    def update(self):
        pass
