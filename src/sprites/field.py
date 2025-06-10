from typing import TYPE_CHECKING
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

        pg.draw.rect(self.image, (255, 255, 255), pg.Rect(0, 0, 1000, 1000), 1)

    def _get_offset_from_coordinates(self, x: int, y: int):
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
        self.field = {}
        x, y = self._get_start_position()

        center_pos: tuple[int, int] = (0, 0)
        while not (center_pos[0] > 1000 or center_pos[1] > 1000):
            center_pos: tuple[int, int] = self._get_tile_center_pos(y + 1)
            self.field[x, y] = Tile(self.game, self.tile_size, int(self.pixel_size * self.camera_distance / 10),
                                    TileTexture.GRASS, self._perspective_angle)
            y += 1

    def _get_start_position(self) -> tuple[int, int]:
        start_y: int = -int(min(
            (self.camera_offset[0] / self._get_half_of_tile_size()[0]) + 1,
            (self.camera_offset[1] / self._get_half_of_tile_size()[1]) + 1
        ))
        start_x: int = 0

        return start_x, start_y

    def _get_tile_center_pos(self, y: int) -> tuple[int, int]:
        return (
            self.camera_offset[0] + self._get_half_of_tile_size()[0] * (y + 1),
            self.camera_offset[1] + self._get_half_of_tile_size()[1] * (y + 1))

    def _get_half_of_tile_size(self) -> tuple[int, int]:
        return Tile.get_half_of_size(self.tile_size, self.pixel_size,
                                     self._perspective_angle, self.camera_distance)

    def update(self):
        pass
