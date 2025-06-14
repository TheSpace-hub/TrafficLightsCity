import logging
from typing import Self
from random import choices, randint
from enum import Enum

from src.sprites import TileTexture


class Direction(Enum):
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    TOP = (0, -1)
    BOTTOM = (0, 1)

    @classmethod
    def get_territory_that_should_be_empty(cls, direction: Self):
        variants: dict[Self, list[tuple[int, int]]] = {
            Direction.RIGHT: [
                (1, -1), (1, 0), (1, 1),
                (2, -1), (2, 0), (2, 1),
            ],
            Direction.LEFT: [
                (-1, -1), (-1, 0), (-1, 1),
                (-2, -1), (-2, 0), (-2, 1),
            ],
            Direction.TOP: [
                (-1, -1), (0, -1), (1, -1),
                (-1, -2), (0, -2), (1, -2),
            ],
            Direction.BOTTOM: [
                (-1, 1), (0, 1), (1, 1),
                (-1, 2), (0, 2), (1, 2),
            ]
        }
        return variants[direction]

    @classmethod
    def get_opposite_direction(cls, direction: Self):
        opposite: dict[Self, Self] = {
            Direction.RIGHT: Direction.LEFT,
            Direction.LEFT: Direction.RIGHT,
            Direction.TOP: Direction.BOTTOM,
            Direction.BOTTOM: Direction.TOP
        }
        return opposite[direction]


class MapGenerator:
    def __init__(self, size: tuple[int, int]):
        if size[0] < 3 or size[1] < 3:
            logging.error('Поле не может быть размером меньше 3x3. (Размер поля: %s)', size)
        self._field: dict[tuple[int, int], TileTexture] = {}
        self._construction_points: list[tuple[int, int]] = [(round(size[0] / 2), round(size[1] // 2))]
        self._size: tuple[int, int] = size

    def generate_map(self) -> dict[tuple[int, int], TileTexture]:
        for x in range(self._size[0]):
            for y in range(self._size[1]):
                self._field[(x, y)] = TileTexture.GRASS
        self._field[(round(self._size[0] / 2), round(self._size[1] // 2))] = TileTexture.ASPHALT

        while len(self._construction_points) > 0:
            for point in self._construction_points[:]:
                self._build_something_from_point(point)
                self._construction_points.remove(point)
        return self._field

    def _build_something_from_point(self, point: tuple[int, int]):
        if point not in self._construction_points:
            logging.warning('Точки %s нет в списке точек для построения', point)
            return

        possible_directions: list[Direction] = self._get_possible_construction_directions(point)
        new_directions = []
        if self._get_directions_of_road(point) == [] or (
                self._get_directions_of_road(point)[0] in possible_directions and randint(0, 4) in [0, 1]):
            k = randint(1, len(possible_directions)) if len(possible_directions) > 1 else len(possible_directions)
            if point == (round(self._size[0] / 2), round(self._size[1] // 2)):
                k = 4
            new_directions = choices(possible_directions, k=k)
        elif self._get_directions_of_road(point) == [] or self._get_directions_of_road(point)[0] in possible_directions:
            new_directions = [self._get_directions_of_road(point)[0]]

        for direction in new_directions:
            self._field[(point[0] + direction.value[0], point[1] + direction.value[1])] = TileTexture.ASPHALT
            self._construction_points.append((point[0] + direction.value[0], point[1] + direction.value[1]))

    def _get_possible_construction_directions(self, point: tuple[int, int]) -> list[Direction]:
        if point not in self._construction_points:
            logging.warning('Точки %s нет в списке точек для построения', point)
            return []

        directions: list[Direction] = []
        for direction in [Direction.RIGHT, Direction.LEFT, Direction.TOP, Direction.BOTTOM]:
            can_build: bool = True
            for check_point in Direction.get_territory_that_should_be_empty(direction):
                x: int = point[0] + check_point[0]
                y: int = point[1] + check_point[1]
                if not (0 < x < self._size[0]) or not (0 < y < self._size[1]) or self._field[
                    (x, y)] != TileTexture.GRASS:
                    can_build = False
                    break
            if can_build:
                directions.append(direction)
        return directions

    def _get_directions_of_road(self, point: tuple[int, int]) -> list[Direction]:
        directions: list[Direction] = []
        for direction in [Direction.RIGHT, Direction.LEFT, Direction.TOP, Direction.BOTTOM]:
            x: int = point[0] + direction.value[0]
            y: int = point[1] + direction.value[1]
            if not (0 < x < self._size[0]) or not (0 < y < self._size[1]):
                continue
            if self._field[(x, y)] == TileTexture.ASPHALT:
                directions.append(Direction.get_opposite_direction(direction))
        return directions
