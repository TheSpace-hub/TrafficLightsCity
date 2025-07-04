from typing import TYPE_CHECKING
from math import pi
import pygame as pg

from src.state import State

from src.sprites import Text, TextAlign, Field, TrafficLight, Button, InBlockText, ButtonStatus, TrafficLightData, \
    Container

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

        self.add_sprite('dashboard', Button(self.game, 1465, 10, 445, 70,
                                            InBlockText(self.game, 'Панель Управ.', 16,
                                                        (255, 255, 255)),
                                            self.on_dashboard_button_pressed))
        self.add_traffic_lights_build_buttons()

    def update(self):
        field: Field = self.get_sprite('field')
        if pg.key.get_pressed()[pg.K_u]:
            field.perspective_angle = min(field.perspective_angle + 0.1, pi / 4)
            field.view_field = {}
            field.update_view()
        if pg.key.get_pressed()[pg.K_j]:
            field.perspective_angle = max(field.perspective_angle - 0.1, 0.3)
            field.view_field = {}
            field.update_view()

        if 5 in self.game.omitted_mouse_buttons:
            field.change_camera_distance(-.1)
        elif 4 in self.game.omitted_mouse_buttons:
            field.change_camera_distance(.1)

        if (pg.key.get_pressed()[pg.K_w] or pg.key.get_pressed()[pg.K_s] or pg.key.get_pressed()[pg.K_a] or
                pg.key.get_pressed()[pg.K_d]):
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
                            direction[key][0] * field.move_speed * field.get_camera_distance()),
                        field.camera_offset[1] + int(
                            direction[key][1] * field.move_speed * field.get_camera_distance()))
            field.update_view()

    def add_traffic_lights_build_buttons(self):
        traffic_lights: list[TrafficLight] = [TrafficLight(self.game, t) for t in TrafficLightData.get_all_types()]
        for i in range(len(traffic_lights)):
            self.add_sprite(f'traffic_light_{traffic_lights[i].data.tfl_type}_build',
                            Button(self.game, 10 + i * 110, 970, 100, 100,
                                   InBlockText(self.game, '', 0, (0, 0, 0)),
                                   placeholder=traffic_lights[i].get_cover))

    def enter(self):
        field_sizes: dict[str, tuple[int, int]] = {
            'small': (30, 30),
            'medium': (50, 50),
            'large': (80, 80)
        }
        field_size = self.game.transmitted_data['field_size']
        seed = self.game.transmitted_data['seed']

        field: Field = self.get_sprite('field')
        field.generate_field(seed, field_sizes[field_size])
        field.update_view()

    def on_dashboard_button_pressed(self, status: ButtonStatus):
        if status == ButtonStatus.PRESSED:
            self.game.change_state('Dashboard')

    def exit(self):
        pass
