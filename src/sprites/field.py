import logging
from typing import TYPE_CHECKING
from math import cos, sin, sqrt, radians
import pygame as pg

from src.sprite import Sprite
from src.sprites import Tile, TileTexture, Text

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
            self.image.blit(tile.image, self._get_offset_from_coordinates(pos[0], pos[1]))

        if self.debug_view_mode:
            self._draw_zero_vectors()

    def change_camera_distance(self, distance: float):
        if not (0.5 <= distance <= 2):
            return
        self._camera_distance = round(distance, 1)
        self.view_field = {}
        self.update_view()

    def get_camera_distance(self) -> float:
        return self._camera_distance

    def generate_field(self, seed: int | None = None):
        self.view_field = {}
        self.field = MapGenerator((30, 30), seed).generate_map()

    # TODO - когда угол перспективы такой, что ось y, проведённая при неизменном x не по подает в угол
    #  экрана, то карта не заполняется полностью.
    def _update_tiles(self):
        updated_pos: list[tuple[int, int]] = []
        x, y = self._get_position_of_beginning_of_construction()

        for delta_y in [1, -1]:
            y = self._get_position_of_beginning_of_construction()[1]
            while not self._does_tile_extend_beyond_field(x, y):
                updated_pos.append((x, y))
                x = self._get_position_of_beginning_of_construction()[0]
                for delta_x in [1, -1]:
                    while not self._does_tile_extend_beyond_field(x, y):
                        x += delta_x
                        updated_pos.append((x, y))
                    x = self._get_position_of_beginning_of_construction()[0]
                y += delta_y

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
        yx = round(self._get_half_of_tile_size()[0] / 2)
        yy = round(self._get_half_of_tile_size()[1] / 2)
        xx = round(self._get_half_of_tile_size()[0] / 2)
        xy = -round(self._get_half_of_tile_size()[1] / 2)
        return (xx, xy), (yx, yy)

    def _get_offset_from_coordinates(self, x: int, y: int):
        """
        Получить координаты на экране в зависимости от координат тайла и смещения камеры
        """
        return (self.camera_offset[0] + self._get_half_of_tile_size()[0] * (x + y),
                self.camera_offset[1] + self._get_half_of_tile_size()[1] * (y - x))

    def _get_position_of_beginning_of_construction(self) -> tuple[int, int]:
        """
        Наход координаты тайла с которого стоит начинать строительство карты.
        Оптимальный тайл находится на середине карты.

        Решение системы уравнений из (1) и (2):
        (1) k1 = (WxUy - WyUx) / (UxVy - UyVx)
        (2) k2 = (UxWy - UyWx) / (UxVy - UyVx)
        Где k1 - кол-во векторов "y" и k2 - кол-во векторов "x"

        Вектора w - вектор от тайла (0, 0), u - вектор x, v - вектор y
        """
        wx = 960 - self._get_offset_from_coordinates(0, 0)[0]
        wy = 540 - self._get_offset_from_coordinates(0, 0)[1]
        ux = self._get_zero_vector()[0][0] * 2
        uy = self._get_zero_vector()[0][1] * 2
        vx = self._get_zero_vector()[1][0] * 2
        vy = self._get_zero_vector()[1][1] * 2

        x, y = round((wx * vy - wy * vx) / (ux * vy - uy * vx)), round((ux * wy - uy * wx) / (ux * vy - uy * vx)) - 1
        while self._does_tile_extend_beyond_field(x, y):
            y += 1
        return x, y

    def _get_position_of_ending_of_construction(self) -> tuple[int, int]:
        """
        Решение системы уравнений из (1) и (2):
        (1) k1 = (WxUy - WyUx) / (UxVy - UyVx)
        (2) k2 = (UxWy - UyWx) / (UxVy - UyVx)
        Где k1 - кол-во векторов "y" и k2 - кол-во векторов "x"

        Вектора w - вектор от тайла (0, 0), u - вектор x, v - вектор y
        """
        wx = self._get_half_of_tile_size()[0] - self._get_offset_from_coordinates(0, 0)[0] - \
             self._get_half_of_tile_size()[0]
        wy = self._get_half_of_tile_size()[1] - self._get_offset_from_coordinates(0, 0)[1] - \
             self._get_half_of_tile_size()[1]
        ux = self._get_zero_vector()[0][0] * 2
        uy = self._get_zero_vector()[0][1] * 2
        vx = self._get_zero_vector()[1][0] * 2
        vy = self._get_zero_vector()[1][1] * 2

        x, y = round((wx * vy - wy * vx) / (ux * vy - uy * vx)), round((ux * wy - uy * wx) / (ux * vy - uy * vx)) - 1
        while self._does_tile_extend_beyond_field(x, y):
            y += 1
        return x, y

    def _get_tile_center_pos(self, x: int, y: int) -> tuple[int, int]:
        return (
            self._get_offset_from_coordinates(x, y)[0] + self._get_half_of_tile_size()[0],
            self._get_offset_from_coordinates(x, y)[1] + self._get_half_of_tile_size()[1]
        )

    def _get_half_of_tile_size(self) -> tuple[int, int]:
        return Tile.get_half_of_size(self.tile_size, self.pixel_size,
                                     self.perspective_angle, self._camera_distance)

    def _does_tile_extend_beyond_field(self, x: int, y: int) -> bool:
        return not (self._get_offset_from_coordinates(x, y)[0] < 1920 and self._get_offset_from_coordinates(x, y)[
            1] < 1080
                    and self._get_offset_from_coordinates(x, y)[0] + 2 * self._get_half_of_tile_size()[0] > 0 and
                    self._get_offset_from_coordinates(x, y)[1] + 2 * self._get_half_of_tile_size()[1] > 0)

    def update(self):
        pass
