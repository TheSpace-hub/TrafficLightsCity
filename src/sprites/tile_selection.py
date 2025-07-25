from typing import TYPE_CHECKING, Callable, Optional
import pygame as pg

from src.sprite import Sprite

if TYPE_CHECKING:
    from src.game import Game
    from src.sprites import Field


class TileSelection(Sprite):
    def __init__(self, game: 'Game', filed: 'Field', func: Callable[[tuple[int, int]], None] | None):
        super().__init__(game, (1920, 1080))
        self.field: 'Field' = filed
        self.func: Callable[[tuple[int, int]], None] | None = func
        self._visible: bool = False
        self.limits: pg.Rect = pg.Rect(30, 30, 1860, 910)

    def update_view(self):
        self.image = pg.Surface((1920, 1080), pg.SRCALPHA, 32).convert_alpha()

        pg.draw.rect(self.image, (128, 128, 128), self.limits, 3)

        if not self.limits.collidepoint(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]):
            return

        coord: tuple[int, int] = self.field.get_offset_from_coordinates(self.get_coord())
        polygon: list[tuple[int, int]] = list(
            map(lambda pos: (pos[0] + coord[0], pos[1] + coord[1]), self.field.get_tile_as_polygon()))
        pg.draw.polygon(self.image, (255, 255, 255), polygon, 3)

    def is_visible(self) -> bool:
        return self._visible

    def set_visible(self, visible: bool):
        self.image = pg.Surface((1920, 1080), pg.SRCALPHA, 32).convert_alpha()
        self._visible = visible

    def get_coord(self) -> Optional[tuple[int, int]]:
        if not self.limits.collidepoint(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]):
            return None
        return self.field.get_tile_position_by_coordinates(pg.mouse.get_pos())

    def update(self):
        if self._visible:
            self.update_view()
            if 1 in self.game.omitted_mouse_buttons and self.func is not None:
                self.func(self.get_coord())
