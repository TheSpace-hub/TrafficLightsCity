from typing import TYPE_CHECKING
from os import path
import json
import pygame as pg

from src.sprites import Pixelart
from src.sprite import Sprite

if TYPE_CHECKING:
    from src.game import Game


class TrafficLightSegment:
    def __init__(self, pos: tuple[int, int], texture: str, value: str | None = None):
        self.pos: tuple[int, int] = pos
        self.texture: str = texture
        self.value: str = self._get_values()[0] if value is None else value

    def get_pixelart_by_value(self, value: str) -> tuple[tuple[tuple[int, int, int, int], ...]]:
        return self._get_texture()[value]

    def _get_values(self) -> list[str]:
        return list(self._get_texture().keys())

    def _get_texture(self) -> dict:
        data: dict = {}
        with open(path.join('saves', 'traffic_lights', 'textures', f'{self.texture}.json')) as file:
            data = json.loads(file.read())
        return data

    def __str__(self):
        return f'"pos": {self.pos}, "texture": {self.texture}, "value": {self.value}"'

    def __repr__(self):
        return self.__str__()


class TrafficLightData:
    def __init__(self, tfl_type: str):
        self.tfl_type: str = tfl_type
        data: dict = self._get_traffic_light_data()

        self.url: str = data['url']
        self.type_use: bool = self._get_type_use(data)
        self.type_value: str = self._get_type_value(data)
        self.segments: dict[str, TrafficLightSegment] = self._get_segments(data)
        self.states: list[dict[str, str]] = self._get_states(data)

    def _get_traffic_light_data(self) -> dict:
        with open(path.join('saves', 'traffic_lights', f'{self.tfl_type}.json'), 'r') as file:
            return json.loads(file.read())

    @staticmethod
    def _get_url(data: dict) -> str:
        return str(data['url'])

    @staticmethod
    def _get_type_use(data: dict) -> bool:
        return bool(data['type']['use'])

    @staticmethod
    def _get_type_value(data: dict) -> str:
        return str(data['type']['value'])

    @staticmethod
    def _get_segments(data: dict) -> dict[str, TrafficLightSegment]:
        segments: dict[str, TrafficLightSegment] = {}
        for name, segment in data['segments'].items():
            segments[name] = TrafficLightSegment(
                (int(segment['pos']['x']), int(segment['pos']['y'])),
                str(segment['texture'])
            )
        return segments

    @staticmethod
    def _get_states(data: dict) -> list[dict[str, str]]:
        states: list[dict[str, str]] = []
        for state in data['states']:
            states.append(state)
        return states

    def get_size(self) -> tuple[int, int]:
        size: tuple[int, int] = (1, 1)
        for segment in self.segments.values():
            size = (max(size[0], segment.pos[0] + 1), max(size[1], segment.pos[1] + 1))
        return size

    def __str__(self):
        return (f'"url": {self.url}, '
                f'"use": {self.type_use}, '
                f'"value": {self.type_value}, '
                f'"segments": {self.segments},'
                f'"states": {self.states}')


class TrafficLight(Sprite):
    def __init__(self, game: 'Game', tfl_type: str):
        super().__init__(game, (0, 0), (0, 0))
        self.game: 'Game' = game
        self.data = TrafficLightData(tfl_type)
        self.as_cover: bool = True

        self.update_view()

    def update_view(self):
        if self.as_cover:
            self.image = self.get_cover()

    def get_cover(self, image_size: tuple[int, int] = (30, 30)) -> pg.Surface:
        surface: pg.Surface = pg.Surface(
            (self.data.get_size()[0] * image_size[0], self.data.get_size()[1] * image_size[1]))
        for segment in self.data.segments.values():
            pixelart: tuple[tuple[tuple[int, int, int, int], ...]] = segment.get_pixelart_by_value(segment.value)
            pixel_size: float = min(image_size[0] / len(pixelart[0]), image_size[1] / len(pixelart[1]))
            surface.blit(Pixelart(self.game, (0, len(self.data.segments.values()) * 1), image_size,
                                  pixelart).image, (0, pixel_size * len(pixelart[0])))

        return surface

    def update(self):
        pass
