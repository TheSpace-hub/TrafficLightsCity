import logging
from enum import Enum

from src.sprites import TileTexture


class Direction(Enum):
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    TOP = (0, -1)
    BOTTOM = (0, 1)


class MapGenerator:
    def __init__(self, size: tuple[int, int]):
        if size[0] < 3 or size[1] < 3:
            logging.error('Поле не может быть размером меньше 3x3. (Размер поля: %s)', size)
        self._field: dict[tuple[int, int], TileTexture] = {}
        self._construction_points: list[tuple[int, int]] = []
        self._size: tuple[int, int] = size

    def generate_map(self) -> dict[tuple[int, int], TileTexture]:
        for x in range(self._size[0]):
            for y in range(self._size[1]):
                self._field[(x, y)] = TileTexture.GRASS
        self._field[(round(self._size[0] / 2), round(self._size[1] // 2))] = TileTexture.ASPHALT

        self._construction_points.append((round(self._size[0] / 2) + 1, round(self._size[1] // 2)))
        self._construction_points.append((round(self._size[0] / 2) - 1, round(self._size[1] // 2)))
        self._construction_points.append((round(self._size[0] / 2), round(self._size[1] // 2) + 1))
        self._construction_points.append((round(self._size[0] / 2), round(self._size[1] // 2) - 1))

        # while len(self._construction_points) > 0:
        #     for point in self._construction_points[:]:
        #         self._build_something_from_point(point)

        return self._field

    def _build_something_from_point(self, point: tuple[int, int]):
        if point not in self._construction_points:
            logging.warning('Точки %s нет в списке точек для построения', point)
            return

    def _get_possible_construction_directions(self, point: tuple[int, int]) -> list[Direction]:
        if point not in self._construction_points:
            logging.warning('Точки %s нет в списке точек для построения', point)
            return []

        directions: list[Direction] = []
        for direction in [Direction.RIGHT, Direction.LEFT, Direction.TOP, Direction.BOTTOM]:
            can_build: bool = True
            for x in range(point[0] - 1 + direction.value[0], point[0] + 2 + direction.value[0]):
                if not can_build:
                    break
                for y in range(point[1] - 1 + direction.value[1], point[1] + 2 + direction.value[1]):
                    if (x, y) == point:
                        continue
                    if self._field[(x, y)] != TileTexture.GRASS:
                        can_build = False
                        break
            if can_build:
                directions.append(direction)
        return directions
