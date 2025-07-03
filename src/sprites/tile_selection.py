from typing import TYPE_CHECKING
import pygame as pg

from src.sprite import Sprite

if TYPE_CHECKING:
    from src.game import Game
    from src.sprites import Field


class TileSelection(Sprite):
    def __init__(self, game: 'Game', pos: tuple[int, int], size: tuple[int, int], filed: 'Field'):
        super().__init__(game, size, pos)
        self.field: 'Field' = filed
        self.update_view()

    def update_view(self):
        self.image.fill((32, 32, 32))
        coord = self.field.get_offset_from_coordinates(
            self.field.get_tile_position_by_coordinates(pg.mouse.get_pos())
        )
        pg.draw.rect(self.image, (255, 255, 255), pg.Rect(
            coord[0], coord[1], self.field.get_half_of_tile_size()[0] * 2, self.field.get_half_of_tile_size()[1] * 2
        ), 1)

    def update(self):
        pass
