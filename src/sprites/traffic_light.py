from typing import TYPE_CHECKING, Optional, Sequence

import pygame as pg
from pygame import SRCALPHA

from src.sprites import Container
from src.sprite import Sprite

from src.modules import TrafficLightData, TrafficLightSegment

if TYPE_CHECKING:
    from src.game import Game
    from src.sprites import Field


class TrafficLight(Sprite):
    """
    Основной класс светофора.
    Может быть добавлен на карту города, или на панель.
    """

    def __init__(self, game: 'Game', tfl_type: str, uuid: Optional[str] = None,
                 field: Optional['Field'] = None):
        super().__init__(game, (0, 0), (0, 0))
        self.game: 'Game' = game
        self.field: Optional['Field'] = field
        self.data = TrafficLightData(tfl_type, uuid)

        self.update_view()

    def update_view(self):
        if self.field is None:
            return
        half_ts = self.field.get_half_of_tile_size()
        self.image = pg.Surface((
            half_ts[0] * .25 + 5 + (self.data.get_size()[0] - 1) * half_ts[0] * .25,
            half_ts[1] * .75 + 5 + (self.data.get_size()[1] - 1) * half_ts[1] * .5
        ),
            pg.SRCALPHA, 32).convert_alpha()

        for segment in self.data.segments.values():
            self._draw_substrate(segment)
        for segment in self.data.segments.values():
            self._draw_appearance(segment)

    def _draw_substrate(self, segment: TrafficLightSegment):
        half_ts = self.field.get_half_of_tile_size()
        displaced_back: Sequence[tuple[float, float]] = list(
            map(lambda p: (
                p[0] + segment.pos[0] * half_ts[0] * .25,
                p[1] + segment.pos[1] * half_ts[1] * .5 - segment.pos[0] * half_ts[1] * .25
            ), [
                    (half_ts[0] * .25, 0),
                    (0, half_ts[1] * .25),
                    (0, half_ts[1] * 0.75),
                    (5, half_ts[1] * 0.75 + 5),
                    (half_ts[0] * .25 + 5, 5),
                ]))
        pg.draw.polygon(self.image, (0, 0, 0), displaced_back)
        pg.draw.polygon(self.image, (0, 0, 0), displaced_back, 3)

    def _draw_appearance(self, segment: TrafficLightSegment):
        half_ts = self.field.get_half_of_tile_size()
        displaced_font: Sequence[tuple[float, float]] = list(
            map(lambda p: (
                p[0] + 5 + segment.pos[0] * half_ts[0] * .25,
                p[1] + 5 + segment.pos[1] * half_ts[1] * .5 - segment.pos[0] * half_ts[1] * .25
            ), [
                    (half_ts[0] * .25, 0),
                    (0, half_ts[1] * .25),
                    (0, half_ts[1] * .75),
                    (half_ts[0] * .25, half_ts[1] * .5)
                ]))

        pg.draw.polygon(self.image, (128, 128, 128), displaced_font)
        pg.draw.polygon(self.image, (0, 0, 0), displaced_font, 3)

        self._draw_appearance_pixelart(segment)

    def _draw_appearance_pixelart(self, segment: TrafficLightSegment):
        pixelart: tuple[tuple[tuple[int, int, int, int], ...]] = segment.get_pixelart_by_value(segment.value)
        half_ts = self.field.get_half_of_tile_size()

        for y, row in enumerate(pixelart):
            for x, color in enumerate(row):
                displaced: Sequence[tuple[float, float]] = list(
                    map(lambda p: (
                        p[0] + 5 + half_ts[0] * ((16 * segment.pos[0] + x) / 64),
                        p[1] + 5 + half_ts[1] * .5 * (segment.pos[1] - segment.pos[0] * .5 + .5 + (2 * y - x) / 32)
                    ), [
                            (half_ts[0] * .25 / 16, 0),
                            (0, half_ts[1] * .25 / 16),
                            (0, half_ts[1] * .75 / 16),
                            (half_ts[0] * .25 / 16, half_ts[1] * .5 / 16)
                        ]))
                if color[3] == 0:
                    color = (128, 128, 128)
                pg.draw.polygon(self.image, color, displaced)

    def get_cover(self, height: int = 94, wight: int | None = 94) -> pg.Surface:
        """
        Получение обложки светофора для отображения в панели
        Arguments:
            height: Высота изображения
            wight: Укажите ширину изображения, если нужно расположить его по центу. Если значение не указано, то ширина будет наименьшей
        Returns:
            Изображение со светофором заданной высоты
        """
        space: int = round(height / self.data.get_size()[1] * 0.1)
        segment_size: int = round(height / self.data.get_size()[1]) - space

        surface_size: tuple[int, int] = (
            wight if wight else round(space + (segment_size + space) * self.data.get_size()[0]), height)
        surface: pg.Surface = pg.Surface(surface_size, SRCALPHA, 32).convert_alpha()
        surface.blit(Container(self.game, (0, 0), (0, 0)).image, (0, 0))

        offset_for_centering: int = (wight - round(
            space + (segment_size + space) * self.data.get_size()[0])) // 2 if wight else 0
        for segment in self.data.segments.values():
            segment_image = segment.get_image_by_value(segment.value, segment_size)
            surface.blit(segment_image,
                         (offset_for_centering + space + segment_size * segment.pos[0] + space * segment.pos[0],
                          space + segment_size * segment.pos[1] + space * segment.pos[1]))

        return surface

    def update(self):
        pass
