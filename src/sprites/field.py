from typing import TYPE_CHECKING
from math import cos, sin, tan, sqrt, radians
import pygame as pg

from src.sprite import Sprite
from src.sprites import Tile, TileTexture

if TYPE_CHECKING:
    from src.game import Game


class Field(Sprite):
    """
    Поле занимает весь экран и состоит из объектов типа Tile
    """

    def __init__(self, game: 'Game'):
        self._perspective_angle = 30
        super().__init__(game, (1920, 1080), (0, 0))
        self.tile_size = 10
        self.pixel_size = 10

        self.camera_distance: int = 10
        self.camera_offset: tuple[int, int] = (0, 0)

        self.field: dict[tuple[int, int], Tile] = {}

        self.update_view()

    def update_view(self):
        self.image.fill((32, 32, 32))

        self._update_tiles()
        for pos in self.field.keys():
            tile = self.field[pos]
            self.image.blit(tile.image, self._get_offset_from_coordinates(pos[0], pos[1]))

        self._draw_zero_vectors()

    def _draw_zero_vectors(self):
        pg.draw.line(self.image, (255, 0, 0), (960, 540),
                     (960 + self._get_zero_vector()[0][0], 540 + self._get_zero_vector()[0][1]))
        pg.draw.line(self.image, (0, 255, 0), (960, 540),
                     (960 + self._get_zero_vector()[1][0], 540 + self._get_zero_vector()[1][1]))

    def _get_zero_vector(self) -> tuple[tuple[int, int], tuple[int, int]]:
        yx = int(sqrt(1 / (1 + (9 / 16) ** 2)) * 50)
        yy = int(sqrt(1 / (1 + (16 / 9) ** 2)) * 50)
        xx = int(cos(radians(self._perspective_angle)) * 50)
        xy = -int(sin(radians(self._perspective_angle)) * 50)
        return (xx, xy), (yx, yy)

    def _get_offset_from_coordinates(self, x: int, y: int):
        """
        Получить координаты на экране в зависимости от координат тайла и смещения камеры
        """
        return (
            self.camera_offset[0] + self._get_half_of_tile_size()[0] * (x + y),
            self.camera_offset[1] + self._get_half_of_tile_size()[1] * (y - x))

    # TODO - Работает правильно только в случае, когда camera_offset по x и y положительны. Исправить или заблокировать
    #  перемещение по отрицательным координатам
    def _update_tiles(self):
        """
        Обновляет словарь с расположениями тайлов.

        :return:Возвращает True, есть что-то изменилось
        в словаре из тайлов
        """
        updated_field: dict[tuple[int, int], Tile] = {}
        x, y = self._get_position_of_beginning_of_construction()
        print(x, y)

        # center_pos: tuple[int, int] = (0, 0)
        # while not (center_pos[0] > 1920 or center_pos[1] > 1080):
        #     center_pos: tuple[int, int] = self._get_tile_center_pos(y + 1)
        #     updated_field[x, y] = Tile(self.game, self.tile_size, int(self.pixel_size * self.camera_distance / 10),
        #                                TileTexture.GRASS, self._perspective_angle)
        #     y += 1
        #
        # for last_pos in self.field.keys():
        #     if last_pos in updated_field:
        #         updated_field[last_pos] = self.field[last_pos]
        updated_field[x, y] = Tile(self.game, self.tile_size, int(self.pixel_size * self.camera_distance / 10),
                                   TileTexture.SAND, self._perspective_angle)
        updated_field[0, 0] = Tile(self.game, self.tile_size, int(self.pixel_size * self.camera_distance / 10),
                                   TileTexture.STONE, self._perspective_angle)
        self.field = updated_field

    def _get_position_of_beginning_of_construction(self) -> tuple[int, int]:
        """
        Решение системы уравнений из (1) и (2):
        (1) k1 = (WxUy - WyUx) / (UxVy - UyVx)
        (2) k2 = (UxWy - UyWx) / (UxVy - UyVx)
        Где k1 - кол-во векторов "y" и k2 - кол-во векторов "x"

        Вектора w - вектор от тайла (0, 0), u - вектор x, v - вектор y
        """
        pg.draw.line(self.image, (255, 255, 255), (
            self._get_offset_from_coordinates(0, 0)[0] + self._get_half_of_tile_size()[0],
            self._get_offset_from_coordinates(0, 0)[1] + self._get_half_of_tile_size()[1]),
                     self._get_half_of_tile_size())

        wx = self._get_half_of_tile_size()[0] - self._get_offset_from_coordinates(0, 0)[0] - \
             self._get_half_of_tile_size()[0]
        wy = self._get_half_of_tile_size()[1] - self._get_offset_from_coordinates(0, 0)[1] - \
             self._get_half_of_tile_size()[1]
        ux = self._get_zero_vector()[0][0] * 2
        uy = self._get_zero_vector()[0][1] * 2
        vx = self._get_zero_vector()[1][0] * 2
        vy = self._get_zero_vector()[1][1] * 2
        return round((wx * vy - wy * vx) / (ux * vy - uy * vx)), round((ux * wy - uy * wx) / (ux * vy - uy * vx))

    def _get_tile_center_pos(self, y: int) -> tuple[int, int]:
        return (
            self.camera_offset[0] + self._get_half_of_tile_size()[0] * (y + 1),
            self.camera_offset[1] + self._get_half_of_tile_size()[1] * (y + 1))

    def _get_half_of_tile_size(self) -> tuple[int, int]:
        return Tile.get_half_of_size(self.tile_size, self.pixel_size,
                                     self._perspective_angle, self.camera_distance)

    def update(self):
        pass
