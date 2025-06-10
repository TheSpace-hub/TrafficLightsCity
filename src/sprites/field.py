from typing import TYPE_CHECKING
from math import sin, cos, sqrt, radians

from src.sprite import Sprite
from src.sprites import Tile, TileTexture

if TYPE_CHECKING:
    from src.game import Game


class Field(Sprite):
    """
    Поле. Состоит из объектов типа Tile
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
            self.image.blit(tile.image,
                            (
                                self.camera_offset[0] + pos[1] * int(
                                    self.tile_size * self.pixel_size * self.camera_distance / 10 * cos(
                                        radians(self._perspective_angle))),
                                self.camera_offset[1] + pos[1] * int(
                                    self.tile_size * self.pixel_size * self.camera_distance / 10 * sin(
                                        radians(self._perspective_angle)))))

    def _update_tiles(self):
        """
        Обновляет словарь с расположениями тайлов.

        :return:Возвращает True, есть что-то изменилось
        в словаре из тайлов
        """
        if self.field != {}:
            return

        y_iterations: tuple[int, int] = (0, round(max(
            1920 / int(self.tile_size * self.pixel_size * cos(radians(self._perspective_angle))) - 1,
            1080 / int(self.tile_size * self.pixel_size * sin(radians(self._perspective_angle))) - 1
        )))

        for y in range(y_iterations[0], y_iterations[1]):
            self.field[(0, y)] = Tile(self.game, self.tile_size, int(self.pixel_size * self.camera_distance / 10),
                                      TileTexture.GRASS, self._perspective_angle)

    def update(self):
        pass
