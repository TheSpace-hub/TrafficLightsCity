from typing import TYPE_CHECKING
import pygame as pg

from src.state import State

from src.sprites import Text, TextAlign, Field

if TYPE_CHECKING:
    from src.game import Game


class City(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)

    def boot(self):
        self.add_sprite('field', Field(self.game))

        self.add_sprite('city_name', Text(self.game, (10, 10), 'City.01', 16,
                                          (255, 255, 255), align=TextAlign.LEFT))

    def update(self):
        if 5 in self.game.omitted_mouse_buttons:
            field: Field = self.get_sprite('field')
            field.change_camera_distance(field.get_camera_distance() - 1)
        elif 4 in self.game.omitted_mouse_buttons:
            field: Field = self.get_sprite('field')
            field.change_camera_distance(field.get_camera_distance() + 1)

        if (pg.key.get_pressed()[pg.K_w] or pg.key.get_pressed()[pg.K_s] or pg.key.get_pressed()[pg.K_a] or
                pg.key.get_pressed()[pg.K_d]):
            field: Field = self.get_sprite('field')
            direction: dict[int, tuple[int, int]] = {
                pg.K_w: (0, 1),
                pg.K_s: (0, -1),
                pg.K_a: (1, 0),
                pg.K_d: (-1, 0)
            }
            for key in [pg.K_w, pg.K_s, pg.K_a, pg.K_d]:
                if pg.key.get_pressed()[key]:
                    field.camera_offset = (
                        field.camera_offset[0] + int(
                            direction[key][0] * field.move_speed * field.get_camera_distance() / 10),
                        field.camera_offset[1] + int(
                            direction[key][1] * field.move_speed * field.get_camera_distance() / 10))
            field.update_view()

    def enter(self):
        pass

    def exit(self):
        pass
