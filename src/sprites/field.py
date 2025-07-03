from typing import TYPE_CHECKING
import pygame as pg

from src.sprite import Sprite
from src.sprites import Tile, TileTexture

from src.modules import MapGenerator

if TYPE_CHECKING:
    from src.game import Game


class Field(Sprite):
    """
    Поле занимает весь экран и состоит из объектов типа Tile
    """

    def __init__(self, game: 'Game'):
        super().__init__(game, (1920, 1080), (0, 0))
        self.tile_size = 10
        self.pixel_size = 9

        self.perspective_angle = 0.52
        self._camera_distance: float = 1
        self.camera_offset: tuple[int, int] = (0, 0)
        self.move_speed: int = 15
        self.debug_view_mode: bool = False

        self.field: dict[tuple[int, int], TileTexture] = {}
        self.view_field: dict[tuple[int, int], Tile] = {}

        self.update_view()

    def update_view(self):
        self.image.fill((32, 32, 32))

        self._update_tiles()
        for pos in self.view_field.keys():
            tile = self.view_field[pos]
            self.image.blit(tile.image, self.get_offset_from_coordinates(pos))

        if self.debug_view_mode:
            self._draw_zero_vectors()

    def get_tile_position_by_coordinates(self, coord: tuple[int, int]) -> tuple[int, int]:
        """
        Получение координаты тайла на поле по координатам точки на экране

        Решение системы уравнений из (1) и (2):
        (1) k1 = (WxUy - WyUx) / (UxVy - UyVx)
        (2) k2 = (UxWy - UyWx) / (UxVy - UyVx)
        Где k1 - кол-во векторов "y" и k2 - кол-во векторов "x"

        Вектора w - вектор от тайла (0, 0), u - вектор x, v - вектор y
        """
        wx = coord[0] - self.get_offset_from_coordinates((0, 0))[0]
        wy = coord[1] - self.get_offset_from_coordinates((0, 0))[1]
        ux = self._get_zero_vector()[0][0] * 2
        uy = self._get_zero_vector()[0][1] * 2
        vx = self._get_zero_vector()[1][0] * 2
        vy = self._get_zero_vector()[1][1] * 2

        coord = round((wx * vy - wy * vx) / (ux * vy - uy * vx)), round((ux * wy - uy * wx) / (ux * vy - uy * vx)) - 1
        while self._does_tile_extend_beyond_field(coord):
            coord = (coord[0], coord[1] + 1)
        return coord

    def change_camera_distance(self, offset: float):
        if not (0.5 <= self._camera_distance + offset <= 2):
            return

        location_of_zero_tile_before: tuple[int, int] = self._get_position_of_beginning_of_construction()

        self._camera_distance = round(self._camera_distance + offset, 1)

        position_of_zero_tile_after: tuple[int, int] = self.get_offset_from_coordinates(location_of_zero_tile_before)

        deviation: tuple[int, int] = (960 - position_of_zero_tile_after[0],
                                      540 - position_of_zero_tile_after[1])
        self.camera_offset = (self.camera_offset[0] + deviation[0], self.camera_offset[1] + deviation[1])

        self.view_field = {}
        self.update_view()

    def get_camera_distance(self) -> float:
        return self._camera_distance

    def generate_field(self, seed: int | None = None, field_size: tuple[int, int] = (30, 30)):
        self.view_field = {}
        self.field = MapGenerator(field_size, seed).generate_map()

    def get_offset_from_coordinates(self, coord: tuple[int, int]):
        """
        Получить координаты на экране в зависимости от координат тайла и смещения камеры
        """
        return (self.camera_offset[0] + self.get_half_of_tile_size()[0] * (coord[0] + coord[1]),
                self.camera_offset[1] + self.get_half_of_tile_size()[1] * (coord[1] - coord[0]))

    def get_half_of_tile_size(self) -> tuple[int, int]:
        return Tile.get_half_of_size(self.tile_size, self.pixel_size,
                                     self.perspective_angle, self._camera_distance)

    def get_tile_as_polygon(self) -> list[tuple[int, int]]:
        return [
            (0, self.get_half_of_tile_size()[1]),
            (self.get_half_of_tile_size()[0], 0),
            (self.get_half_of_tile_size()[0] * 2, self.get_half_of_tile_size()[1]),
            (self.get_half_of_tile_size()[0], self.get_half_of_tile_size()[1] * 2)
        ]

    def _get_number_of_initial_tiles(self) -> int:
        updated_pos: list[tuple[int, int]] = []
        coord = self._get_position_of_beginning_of_construction()

        for delta_y in [1, -1]:
            coord = (coord[0], self._get_position_of_beginning_of_construction()[1])
            while not self._does_tile_extend_beyond_field(coord):
                updated_pos.append(coord)
                coord = (coord[0], coord[1] + delta_y)

        return len(updated_pos)

    # TODO - когда угол перспективы такой, что ось y, проведённая при неизменном x не по подает в угол
    #  экрана, то карта не заполняется полностью.
    #  P.S. Можно сделать 2 начальных тайла в правом нижнем и левом верхнем углах
    def _update_tiles(self):
        updated_pos: list[tuple[int, int]] = []
        coord: tuple[int, int] = self._get_position_of_beginning_of_construction()

        for delta_y in [1, -1]:
            coord = (coord[0], self._get_position_of_beginning_of_construction()[1])
            while not self._does_tile_extend_beyond_field(coord):
                updated_pos.append(coord)
                coord = (self._get_position_of_beginning_of_construction()[0], coord[1])
                for delta_x in [1, -1]:
                    while not self._does_tile_extend_beyond_field(coord):
                        coord = (coord[0] + delta_x, coord[1])
                        updated_pos.append(coord)
                    coord = (self._get_position_of_beginning_of_construction()[0], coord[1])
                coord = (coord[0], coord[1] + delta_y)

        updated_field: dict[tuple[int, int], Tile] = {}
        for pos in updated_pos[:]:
            if pos in self.view_field.keys():
                updated_field[pos] = self.view_field[pos]
            elif pos in self.field:
                updated_field[pos] = Tile(self.game, self.tile_size,
                                          self.pixel_size * self._camera_distance,
                                          self.field[pos], self.perspective_angle)
            else:
                updated_field[pos] = Tile(self.game, self.tile_size,
                                          self.pixel_size * self._camera_distance,
                                          TileTexture.GRASS, self.perspective_angle)

        self.view_field = updated_field

    def _draw_zero_vectors(self):
        pg.draw.line(self.image, (255, 0, 0), (960, 540),
                     (960 + self._get_zero_vector()[0][0], 540 + self._get_zero_vector()[0][1]))
        pg.draw.line(self.image, (0, 255, 0), (960, 540),
                     (960 + self._get_zero_vector()[1][0], 540 + self._get_zero_vector()[1][1]))

    def _get_zero_vector(self) -> tuple[tuple[int, int], tuple[int, int]]:
        yx = round(self.get_half_of_tile_size()[0] / 2)
        yy = round(self.get_half_of_tile_size()[1] / 2)
        xx = round(self.get_half_of_tile_size()[0] / 2)
        xy = -round(self.get_half_of_tile_size()[1] / 2)
        return (xx, xy), (yx, yy)

    def _get_position_of_beginning_of_construction(self) -> tuple[int, int]:
        """
        Наход координаты тайла с которого стоит начинать строительство карты.
        Оптимальный тайл находится на середине карты.
        """
        return self.get_tile_position_by_coordinates((960, 540))

    def _get_tile_center_pos(self, x: int, y: int) -> tuple[int, int]:
        return (
            self.get_offset_from_coordinates((x, y))[0] + self.get_half_of_tile_size()[0],
            self.get_offset_from_coordinates((x, y))[1] + self.get_half_of_tile_size()[1]
        )

    def _does_tile_extend_beyond_field(self, coord: tuple[int, int]) -> bool:
        return not (self.get_offset_from_coordinates(coord)[0] < 1920 and self.get_offset_from_coordinates(coord)[
            1] < 1080
                    and self.get_offset_from_coordinates(coord)[0] + 2 * self.get_half_of_tile_size()[0] > 0 and
                    self.get_offset_from_coordinates(coord)[1] + 2 * self.get_half_of_tile_size()[1] > 0)

    def update(self):
        pass
