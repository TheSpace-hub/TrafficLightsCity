from dataclasses import field
from typing import TYPE_CHECKING
from math import pi
import pygame as pg

from src.state import State

from src.sprites import Text, TextAlign, Field, Tile, TileTexture

if TYPE_CHECKING:
    from src.game import Game


class City(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.a = 0.52

    def boot(self):
        self.add_sprite('field', Field(self.game))

        self.add_sprite('city_name', Text(self.game, (10, 10), 'City.01', 16,
                                          (255, 255, 255), align=TextAlign.LEFT))

        self.add_sprite('debug_camera_distance_text', Text(self.game, (10, 30), '0', 16,
                                                           (255, 255, 255), align=TextAlign.LEFT))

    def update(self):
        field: Field = self.get_sprite('field')
        if pg.key.get_pressed()[pg.K_w]:
            field.perspective_angle = min(field.perspective_angle + 0.01, pi / 4)
            field.view_field = {}
            field.update_view()
            print(field.perspective_angle)
        if pg.key.get_pressed()[pg.K_s]:
            field.perspective_angle = max(field.perspective_angle - 0.01, 0.3)
            field.view_field = {}
            field.update_view()
            print(field.perspective_angle)

        # if 5 in self.game.omitted_mouse_buttons:
        #     field: Field = self.get_sprite('field')
        #     field.change_camera_distance(field.get_camera_distance() - 1)
        # elif 4 in self.game.omitted_mouse_buttons:
        #     field: Field = self.get_sprite('field')
        #     field.change_camera_distance(field.get_camera_distance() + 1)
        #
        # if (pg.key.get_pressed()[pg.K_w] or pg.key.get_pressed()[pg.K_s] or pg.key.get_pressed()[pg.K_a] or
        #         pg.key.get_pressed()[pg.K_d]):
        #     field: Field = self.get_sprite('field')
        #     direction: dict[int, tuple[int, int]] = {
        #         pg.K_w: (0, 1),
        #         pg.K_s: (0, -1),
        #         pg.K_a: (1, 0),
        #         pg.K_d: (-1, 0)
        #     }
        #     for key in [pg.K_w, pg.K_s, pg.K_a, pg.K_d]:
        #         if pg.key.get_pressed()[key]:
        #             field.camera_offset = (
        #                 field.camera_offset[0] + int(
        #                     direction[key][0] * field.move_speed * field.get_camera_distance() / 10),
        #                 field.camera_offset[1] + int(
        #                     direction[key][1] * field.move_speed * field.get_camera_distance() / 10))
        #     field.update_view()
        #
        # field: Field = self.get_sprite('field')
        # debug_camera_distance_text: Text = self.get_sprite('debug_camera_distance_text')
        # debug_camera_distance_text.text = str(field.get_camera_distance())
        # debug_camera_distance_text.update_view()

    def enter(self):
        pass
        # field: Field = self.get_sprite('field')
        #
        # seed = None
        # if 'seed' in self.game.transmitted_data and type(self.game.transmitted_data['seed']) == int:
        #     seed = self.game.transmitted_data['seed']
        # field.generate_field(seed)
        # field.update_view()

    def exit(self):
        pass
