import logging
from typing import Optional

from enum import Enum
from os import path
from pathlib import Path
import json
from math import ceil

import pygame as pg
from pygame import SRCALPHA

from src.sprites.pixelart import Pixelart


class NoteType(Enum):
    EXCLAMATION_ERROR = 0
    WAIT_MARK = 1
    CLOUD_ERROR = 2
    QUESTION_ERROR = 3
    OK = 4


class Note:
    def __init__(self):
        self._level: Optional[NoteType] = NoteType.WAIT_MARK
        self.note: Optional[str] = None

    def set_level(self, level: Optional[NoteType | int]):
        """Установить или удалить записку для светофора.

        Args:
            level: Тип записки для светофора.

        Note:
            Возможные записки:

            - EXCLAMATION_ERROR (0): Ошибка в работе светофора.
            - WAIT_MARK (1): Подключение к облаку.
            - CLOUD_ERROR (2): Ошибка подключения к облаку.
            - QUESTION_ERROR (3): Ошибка невозможности проверки светофора на работоспособность.
        """
        if type(level) == NoteType:
            self._level = level
        elif type(level) == int:
            self._level = NoteType(level)
        elif level is None:
            self._level = None
        else:
            logging.warning('Невозможно установить уровень записки: "%s"', level)

    def get_level(self) -> Optional[NoteType]:
        return self._level

    def get_cover(self, size: tuple[int, int]) -> pg.Surface:
        return self.get_cover_by_level(size, self.get_level())

    @staticmethod
    def get_cover_by_level(size: tuple[int, int], icon_level: Optional[int]) -> pg.Surface:
        """Получение иконки записки.

        Args:
            size: Размер иконки в пикселях
            icon_level: Уровень записки для светофора
        """
        if icon_level is None:
            return pg.Surface((0, 0))
        paths: dict[NoteType, str] = {
            NoteType.EXCLAMATION_ERROR: path.join('assets', 'images', 'exclamation_error.png'),
            NoteType.WAIT_MARK: path.join('assets', 'images', 'wait_mark.png'),
            NoteType.CLOUD_ERROR: path.join('assets', 'images', 'cloud_error.png'),
            NoteType.QUESTION_ERROR: path.join('assets', 'images', 'question_error.png'),
            NoteType.OK: path.join('assets', 'images', 'ok_mark.png'),
        }

        pixel_size: tuple[float, float] = (size[0] / 16, size[1] / 16)

        surface: pg.Surface = pg.Surface(size, SRCALPHA, 32).convert_alpha()

        pixelart = Pixelart.get_pixelart_by_image(paths[NoteType(icon_level)])
        for y in range(len(pixelart)):
            for x in range(len(pixelart[y])):
                pg.draw.rect(surface, pixelart[y][x], pg.Rect(
                    pixel_size[0] * x, pixel_size[1] * y, ceil(pixel_size[0]), ceil(pixel_size[1])
                ))

        return surface


class TrafficLightSegment:
    """
    Информация о сегменте светофора, также получение изображения секции из текстуры
    """

    def __init__(self, pos: tuple[int, int], texture: str, value: str | None = None):
        self.pos: tuple[int, int] = pos
        self.texture: str = texture
        self.value: str = self._get_values()[0] if value is None else value

    def get_pixelart_by_value(self, value: str) -> tuple[tuple[tuple[int, int, int, int], ...]]:
        return self._get_texture()[value]

    def get_image_by_value(self, value: str, size: int) -> pg.Surface:
        """
        Гарантируется, что изображение будет квадратным
        """
        image: pg.Surface = pg.Surface((size, size), SRCALPHA, 32).convert_alpha()
        pixel_size: float = size / 16

        pixelart: tuple[tuple[tuple[int, int, int, int], ...]] = self.get_pixelart_by_value(value)
        for row in range(len(pixelart)):
            for pixel in range(len(pixelart)):
                pg.draw.rect(image, pixelart[row][pixel], pg.Rect(
                    pixel * pixel_size, row * pixel_size, ceil(pixel_size), ceil(pixel_size)
                ))

        return image

    def _get_values(self) -> list[str]:
        """
        Получение всех возможных вариаций текстуры светофора
        """
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
    """
    Информация о светофоре, основываясь на его типе
    """

    def __init__(self, tfl_type: str, uuid: str | None):
        self.uuid: str | None = uuid
        self.tfl_type: str = tfl_type

        data: dict = self._get_traffic_light_data()

        self.url: str = data['url']
        self.type_use: bool = self._get_type_use(data)
        self.type_value: str = self._get_type_value(data)
        self.segments: dict[str, TrafficLightSegment] = self._get_segments(data)
        self.states: list[dict[str, str]] = self._get_states(data)
        self.current_time: int = 0
        self.note: Note = Note()
        self._state: int = 0

        self._update_segments()

    def get_state(self) -> int:
        return self._state

    def set_state(self, state: int):
        if state != self._state:
            self.current_time = 0
        self._state = state
        self._update_segments()

    @staticmethod
    def get_all_types() -> list[str]:
        return [way.stem for way in Path(path.join('saves', 'traffic_lights')).glob('*.json')]

    def _update_segments(self):
        for name, segment in self.segments.items():
            segment.value = self.states[self._state][name]

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
        """
        Получение размера светофора, где размер одной секции 1x1
        """
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
