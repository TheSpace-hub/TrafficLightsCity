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

        if self.game.lock_mouse:
            field: Field = self.get_sprite('field')
            field.camera_offset = (field.camera_offset[0] + self.game.mouse_offset[0],
                                   field.camera_offset[1] + self.game.mouse_offset[1])
            field.update_view()

        self.game.lock_mouse = pg.mouse.get_pressed()[2]

    def enter(self):
        pass

    def exit(self):
        pass
