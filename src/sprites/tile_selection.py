from typing import TYPE_CHECKING
import pygame as pg

from src.sprite import Sprite

if TYPE_CHECKING:
    from src.game import Game
    from src.sprites import Field


class TileSelection(Sprite):
    def __init__(self, game: 'Game', filed: 'Field'):
        super().__init__(game, (1920, 1080))
        self.field: 'Field' = filed
        self.update_view()

    def update_view(self):
        self.image = pg.Surface((1920, 1080), pg.SRCALPHA, 32).convert_alpha()
        coord = self.field.get_offset_from_coordinates(
            self.field.get_tile_position_by_coordinates(pg.mouse.get_pos())
        )
        polygon: list[tuple[int, int]] = list(
            map(lambda pos: (pos[0] + coord[0], pos[1] + coord[1]), self.field.get_tile_as_polygon()))
        pg.draw.polygon(self.image, (255, 255, 255), polygon, 3)

    def update(self):
        self.update_view()
