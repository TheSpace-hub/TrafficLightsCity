from typing import TYPE_CHECKING, Optional, Sequence

import pygame as pg
from pygame import SRCALPHA

from src.sprites import Container
from src.sprite import Sprite

from src.modules import TrafficLightData

if TYPE_CHECKING:
    from src.game import Game
    from src.sprites import Field


class TrafficLight(Sprite):
    """
    Основной класс светофора.
    Может быть добавлен на карту города, или на панель.
    """

    def __init__(self, game: 'Game', tfl_type: str, uuid: Optional[str] = None, field: Optional['Field'] = None,
                 pos: tuple[int, int] = (0, 0)):
        super().__init__(game, (0, 0), pos)
        self.game: 'Game' = game
        self.field: Optional['Field'] = field
        self.data = TrafficLightData(tfl_type, uuid)
        self.as_cover: bool = True

        self.update_view()

    def update_view(self):
        if self.field is None:
            return
        self.image = pg.Surface((1920, 1080), pg.SRCALPHA, 32).convert_alpha()

        start = [100, 100]
        half_ts = self.field.get_half_of_tile_size()
        front_shape: Sequence[tuple[float, float]] = [
            (half_ts[0] * .25, 0),
            (0, half_ts[1] * .25),
            (0, half_ts[1] * .75),
            (half_ts[0] * .25, half_ts[1] * .5)
        ]

        displaced_back: Sequence[tuple[float, float]] = list(
            map(lambda p: (
                start[0] + p[0] - 5,
                start[1] + p[1] - 5
            ), [
                    (half_ts[0] * .25, 0),
                    (0, half_ts[1] * .25),
                    (0, half_ts[1] * (self.data.get_size()[1] * .5 + .25)),
                    (5, half_ts[1] * (self.data.get_size()[1] * .5 + .25) + 5),
                    (half_ts[0] * .25 + 5, 5),
                ]))

        pg.draw.polygon(self.image, (0, 0, 0), displaced_back)
        for y_segment in range(self.data.get_size()[1]):
            displaced_font: Sequence[tuple[float, float]] = list(
                map(lambda p: (
                    start[0] + p[0],
                    start[1] + p[1] + y_segment * half_ts[1] * .5
                ), front_shape))

            pg.draw.polygon(self.image, (128, 128, 128), displaced_font)
            pg.draw.polygon(self.image, (0, 0, 0), displaced_font, 3)

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
