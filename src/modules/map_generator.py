import logging
from random import choices, randint
from enum import Enum

from src.sprites import TileTexture


class Direction(Enum):
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    TOP = (0, -1)
    BOTTOM = (0, 1)

    @staticmethod
    def get_territory_that_should_be_empty(direction: tuple[int, int]):
        variants: dict[tuple[int, int], list[tuple[int, int]]] = {
            Direction.RIGHT.value: [
                (1, -1), (1, 0), (1, 1),
                (2, -1), (2, 0), (2, 1),
            ],
            Direction.LEFT.value: [
                (-1, -1), (-1, 0), (-1, 1),
                (-2, -1), (-2, 0), (-2, 1),
            ],
            Direction.TOP.value: [
                (-1, -1), (0, -1), (1, -1),
                (-1, -2), (0, -2), (1, -2),
            ],
            Direction.BOTTOM.value: [
                (-1, 1), (0, 1), (1, 1),
                (-1, 2), (0, 2), (1, 2),
            ]
        }
        return variants[direction]


class MapGenerator:
    def __init__(self, size: tuple[int, int], index):
        if size[0] < 3 or size[1] < 3:
            logging.error('Поле не может быть размером меньше 3x3. (Размер поля: %s)', size)
        self._field: dict[tuple[int, int], TileTexture] = {}
        self._construction_points: list[tuple[int, int]] = [(round(size[0] / 2), round(size[1] // 2))]
        self._size: tuple[int, int] = size

        self.index = index

    def generate_map(self) -> dict[tuple[int, int], TileTexture]:
        print('- - - - - Start gen')
        for x in range(self._size[0]):
            for y in range(self._size[1]):
                self._field[(x, y)] = TileTexture.GRASS
        self._field[(round(self._size[0] / 2), round(self._size[1] // 2))] = TileTexture.ASPHALT

        for _ in range(self.index):
            print('- - New step')
            for point in self._construction_points[:]:
                self._build_something_from_point(point)
                self._construction_points.remove(point)
        print('End gen')
        return self._field

    def _build_something_from_point(self, point: tuple[int, int]):
        if point not in self._construction_points:
            logging.warning('Точки %s нет в списке точек для построения', point)
            return
        print(f'Point: {point} with dirs:')

        possible_directions: list[Direction] = self._get_possible_construction_directions(point)
        k = randint(1, len(possible_directions)) if len(possible_directions) > 1 else len(possible_directions)
        for direction in choices(possible_directions, k=k):
            print(f'{direction} ', end='')
            self._field[(point[0] + direction.value[0], point[1] + direction.value[1])] = TileTexture.ASPHALT
            self._construction_points.append((point[0] + direction.value[0], point[1] + direction.value[1]))
        print()

    def _get_possible_construction_directions(self, point: tuple[int, int]) -> list[Direction]:
        if point not in self._construction_points:
            logging.warning('Точки %s нет в списке точек для построения', point)
            return []

        directions: list[Direction] = []
        for direction in [Direction.RIGHT, Direction.LEFT, Direction.TOP, Direction.BOTTOM]:
            can_build: bool = True
            print(
                f' CPoints: {direction}: {direction.value} ({Direction.get_territory_that_should_be_empty(direction.value)}) ')
            for check_point in Direction.get_territory_that_should_be_empty(direction.value):
                x: int = point[0] + check_point[0]
                y: int = point[1] + check_point[1]
                print(f'  self._field[({x}, {y})] == {self._field[(x, y)]}')
                if not (0 < x < self._size[0]) or not (0 < y < self._size[1]) or self._field[
                    (x, y)] != TileTexture.GRASS:
                    can_build = False
                    break
            if can_build:
                print(f'  + Passed. {direction} added')
                directions.append(direction)
        return directions
