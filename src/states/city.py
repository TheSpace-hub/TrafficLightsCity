"""Модуль сцены города.
"""
import json
from typing import TYPE_CHECKING, Optional, Callable
from math import pi
import pygame as pg
from random import randint, choice, uniform
import time
from os import path, listdir

from src.state import State

from src.sprites import Field, TrafficLight, Button, InBlockText, ButtonStatus, TileSelection, \
    TrafficLightInfo, CityInfo, JumpersGroup, Jumper, Pixelart
from src.modules import TrafficLightData

if TYPE_CHECKING:
    from src.game import Game


class SelectorType:
    """Тип селектора, который он может принимать.
    """
    BUILD = 0
    GET_INFO = 1
    REMOVE = 2


class City(State):
    """Сцена города.

    Attributes:
        selected_type_of_selector: При нажатии на кнопку строительства
            светофора здесь, сохраняется информация о выбранном для строительства светофоре.
    """

    def __init__(self, game: 'Game'):
        """Создание сцены города.

        Args:
            game (Game): Экземпляр игры
        """
        super().__init__(game)
        self.selected_type_of_selector: tuple[Optional[int], Optional[str]] = (None, None)
        self.name: str = self.generate_uuid_for_city()
        self.deaths: int = 0
        self.seed: int = 0

    def boot(self):
        """Инициализация сцены.
        """
        filed: Field = self.add_sprite('field', Field(self.game))

        self.add_sprite('tile_selection', TileSelection(self.game, filed, self.apply_selector))
        self.add_sprite('traffic_light_info', TrafficLightInfo(self.game))

        self.add_construction_management_elements_buttons()

        self.add_sprite('city_info', CityInfo(self.game, self.name))

        self.add_sprite('save_map_button', Button(self.game, (10, 120), (400, 50),
                                                  InBlockText(self.game, 'Сохранить карту', 16, (255, 255, 255)),
                                                  self.on_save_map_button_pressed
                                                  ))

        self.add_sprite('jumpers_group', JumpersGroup(self.game))

    def update(self):
        """Обновление сцены.

        Реализация передвижения и ежесекундный пинг.
        """
        self.movement()
        self.pinging()

    def pinging(self):
        """Пинг каждую секунду.
        """
        if time.time() - self.game.last_ping_time >= 1 and self.game.pinger.running:
            jumpers_group: 'JumpersGroup' = self.get_sprite('jumpers_group')
            city_info: 'CityInfo' = self.get_sprite('city_info')
            field: Field = self.get_sprite('field')

            for uuid, result in self.game.pinger.ping().items():
                if result is not None and not result[0]:
                    pos: Optional[tuple[int, int]] = field.get_traffic_light_pos_by_uuid(uuid)
                    if pos is None:
                        continue
                    offset = field.get_offset_from_coordinates(pos)
                    offset = (
                        int(offset[0] + field.get_half_of_tile_size()[0] + uniform(-1, 1) *
                            field.get_half_of_tile_size()[0] / 2 - 15),
                        offset[1] - 30,
                    )
                    jumpers_group.add_jumper(
                        Jumper(self.game, offset, (30, 30),
                               Pixelart.get_pixelart_by_image(
                                   path.join('assets', 'images', 'coffin.png')
                               ))
                    )
                    self.deaths += 1
            city_info.update_info(self.deaths)
            city_info.update_view()
            self.game.last_ping_time = time.time()

            field.update_view()

    def add_construction_management_elements_buttons(self):
        """Добавление кнопок, отвечающих за строительство.
        """
        self.add_info_about_traffic_light_button()
        self.add_remove_traffic_light_button()
        self.add_traffic_lights_build_buttons()

    def add_info_about_traffic_light_button(self):
        """Добавление кнопки для получения информации о светофоре.
        """
        self.add_sprite('info_about_traffic_light', Button(self.game, (10, 970), (100, 100),
                                                           InBlockText(self.game, 'ИНФО', 16, (255, 255, 255)),
                                                           func=self.on_info_about_traffic_light_button_pressed))

    def add_remove_traffic_light_button(self):
        """Добавление кнопки для удаления светофора.
        """
        self.add_sprite('remove_traffic_light', Button(self.game, (120, 970), (100, 100),
                                                       InBlockText(self.game, 'УДАЛ', 16, (255, 255, 255)),
                                                       func=self.on_remove_traffic_light_button_pressed))

    def add_traffic_lights_build_buttons(self):
        """Добавление кнопок всех типов светофоров.
        """
        traffic_lights: list[TrafficLight] = [TrafficLight(self.game, t) for t in TrafficLightData.get_all_types()]

        for i in range(len(traffic_lights)):
            self.add_sprite(f'traffic_light_{traffic_lights[i].data.tfl_type}_build',
                            Button(self.game, (10 + (i + 2) * 110, 970), (100, 100),
                                   InBlockText(self.game, '', 0, (0, 0, 0)),
                                   func=self.on_traffic_light_build_button_pressed,
                                   func_context=traffic_lights[i].data.tfl_type,
                                   placeholder=traffic_lights[i].get_cover))

    def enter(self):
        """Передача сида и размера карты при заходе.
        """
        field_sizes: dict[str, tuple[int, int]] = {
            'small': (30, 30),
            'medium': (50, 50),
            'large': (80, 80)
        }
        field_size = self.game.transmitted_data['field_size']
        self.seed = self.game.transmitted_data['seed']

        if self.seed is None:
            self.seed = randint(0, 9999999999)

        field: Field = self.get_sprite('field')
        field.generate_field(self.seed, field_sizes[field_size])
        field.update_view()
        self.game.pinger.running = True

    def on_dashboard_button_pressed(self, status: ButtonStatus):
        """Переход на сцену при нажатии на кнопку "Панель управления".
        """
        if status == ButtonStatus.PRESSED:
            self.game.change_state('Dashboard')

    def on_traffic_light_build_button_pressed(self, status: ButtonStatus, context: str):
        """Выбор светофора при нажатии на кнопку постройки светофора.
        """
        if status == ButtonStatus.PRESSED:
            self.selected_type_of_selector = (SelectorType.BUILD, context)
            tile_selection: TileSelection = self.get_sprite('tile_selection')
            tile_selection.set_visible(True)

    def on_info_about_traffic_light_button_pressed(self, status: ButtonStatus):
        """Действие при нажатии на кнопку отмены строительства.
        """
        if status == ButtonStatus.PRESSED:
            self.selected_type_of_selector = (SelectorType.GET_INFO, None)
            tile_selection: TileSelection = self.get_sprite('tile_selection')
            tile_selection.set_visible(True)

    def on_remove_traffic_light_button_pressed(self, status: ButtonStatus):
        """Действие при нажатии на кнопку отмены строительства.
        """
        if status == ButtonStatus.PRESSED:
            self.selected_type_of_selector = (SelectorType.REMOVE, None)
            tile_selection: TileSelection = self.get_sprite('tile_selection')
            tile_selection.set_visible(True)

    def on_save_map_button_pressed(self, status: ButtonStatus):
        if status != ButtonStatus.PRESSED:
            return

        city: dict = {
            'name': self.name,
            'deaths': self.deaths,
            'seed': self.seed,
            'traffic_lights': {}
        }
        field: Field = self.get_sprite('field')
        for tfl_type in TrafficLightData.get_all_types():
            city['traffic_lights'][tfl_type] = []
            for pos, traffic_light in field.traffic_lights.items():
                if traffic_light.data.tfl_type == tfl_type:
                    city['traffic_lights'][tfl_type].append(pos)

        with open(path.join('saves', 'maps', f'{self.name}.json'), 'w') as file:
            file.write(json.dumps(city))

    def apply_selector(self, pos: tuple[int, int]):
        actions: dict[int, Callable[[tuple[int, int]], None]] = {
            SelectorType.BUILD: self.build_traffic_light,
            SelectorType.GET_INFO: self.show_traffic_light_info,
            SelectorType.REMOVE: self.remove_traffic_light,
        }
        actions[self.selected_type_of_selector[0]](pos)

    def show_traffic_light_info(self, pos: tuple[int, int]):
        """Отображение информации о светофоре.

        Args:
            pos: Позиция тайла на поле.
        """
        field: Field = self.get_sprite('field')
        if pos not in field.traffic_lights:
            return

        traffic_light_info: 'TrafficLightInfo' = self.get_sprite('traffic_light_info')
        traffic_light_info.data = field.traffic_lights[pos].data
        traffic_light_info.update_view()

    def build_traffic_light(self, pos: tuple[int, int]):
        """Постройка светофора на поле.

        Args:
            pos: Координаты тала на поле.
        """
        field: Field = self.get_sprite('field')
        if not field.can_build_traffic_light(pos):
            return
        uuid: str = self.generate_uuid_for_traffic_light()
        field.traffic_lights[pos] = TrafficLight(self.game, self.selected_type_of_selector[1],
                                                 uuid, field=field)
        field.update_view()

        data = TrafficLightData(self.selected_type_of_selector[1], uuid)

        self.game.pinger.traffic_lights_data.append(data)
        field.traffic_lights[pos].data = data

    def remove_traffic_light(self, pos: tuple[int, int]):
        """Удаление светофора с поля.

        Args:
            pos: Координаты тала на поле.
        """
        field: Field = self.get_sprite('field')
        if not field.can_build_traffic_light(pos):
            return
        if pos not in field.traffic_lights:
            return

        uuid: str = field.traffic_lights[pos].data.uuid
        for i in range(len(self.game.pinger.traffic_lights_data)):
            if self.game.pinger.traffic_lights_data[i].uuid == uuid:
                del self.game.pinger.traffic_lights_data[i]
                break

        field.traffic_lights.pop(pos)
        field.update_view()

    def generate_uuid_for_traffic_light(self) -> str:
        """Создание более интересного уникального uuid для светофора.
        """
        cities: list[str] = [
            "moscow", "saintpetersburg", "novosibirsk", "yekaterinburg", "kazan",
            "nizhnynovgorod", "chelyabinsk", "samara", "omsk", "rostovondon",
            "ufa", "krasnoyarsk", "perm", "voronezh", "volgograd", "krasnodar",
            "saratov", "tyumen", "tolyatti", "izhevsk", "barnaul", "ulyanovsk",
            "irkutsk", "khabarovsk", "yaroslavl", "vladivostok", "makhachkala",
            "tomsk", "orenburg", "kemerovo", "novokuznetsk", "ryazan", "astrakhan",
            "naberezhnyechelny", "penza", "lipetsk", "kirov", "cheboksary",
            "tula", "kaliningrad", "balashikha", "kursk", "stavropol", "sochi",
            "ivanovo", "tver", "bryansk", "belgorod", "arzamas", "vladimir",
            "chita", "grozny", "kaluga", "smolensk", "volzhsky", "murmansks",
            "vladikavkaz", "saransk", "yakutsk", "sterlitamak", "orsk", "severodvinsk",
            "novorossiysk", "nizhnekamsk", "shakhty", "dzerzhinsk", "engels",
            "biysk", "prokopyevsk", "rybinsk", "balakovo", "armavir", "lobnya",
            "seversk", "mezhdurechensk", "kamenskuralsky", "miass", "elektrostal",
            "zlatoust", "serpukhov", "kopeyk", "almetyevsk", "odintsovo", "korolyov",
            "lyubertsy", "kovrov", "novouralsk", "khasavyurt", "pyatigorsk",
            "serov", "arzamas", "berezniki", "kislovodsk", "anapa", "gelendzhik",
            "yeysk", "komsomolsknaamure", "nizhnevartovsk", "novyurengoy",
            "magadan", "norilsk", "salekhard", "surgut", "khanty-mansiysk",
            "yuzhnosakhalinsk", "vorkuta", "nadym", "gubkinsky", "murmansk",
            "severomorsk", "arzamas", "arzamas", "ivanteevka"
        ]
        contains: bool = True
        uuid = f'{choice(cities)}_{randint(1, 999)}'
        while contains:
            contains: bool = False
            for traffic_light in self.game.pinger.traffic_lights_data:
                if traffic_light.uuid == uuid:
                    contains = True
                    uuid = f'{choice(cities)}_{randint(1, 999)}'
                    break

        return uuid

    @staticmethod
    def generate_uuid_for_city() -> str:
        """Создание уникального названия для города.
        """
        cities: list[str] = [
            "moscow", "saintpetersburg", "novosibirsk", "yekaterinburg", "kazan",
            "nizhnynovgorod", "chelyabinsk", "samara", "omsk", "rostovondon",
            "ufa", "krasnoyarsk", "perm", "voronezh", "volgograd", "krasnodar",
            "saratov", "tyumen", "tolyatti", "izhevsk", "barnaul", "ulyanovsk",
            "irkutsk", "khabarovsk", "yaroslavl", "vladivostok", "makhachkala",
            "tomsk", "orenburg", "kemerovo", "novokuznetsk", "ryazan", "astrakhan",
            "naberezhnyechelny", "penza", "lipetsk", "kirov", "cheboksary",
            "tula", "kaliningrad", "balashikha", "kursk", "stavropol", "sochi",
            "ivanovo", "tver", "bryansk", "belgorod", "arzamas", "vladimir",
            "chita", "grozny", "kaluga", "smolensk", "volzhsky", "murmansks",
            "vladikavkaz", "saransk", "yakutsk", "sterlitamak", "orsk", "severodvinsk",
            "novorossiysk", "nizhnekamsk", "shakhty", "dzerzhinsk", "engels",
            "biysk", "prokopyevsk", "rybinsk", "balakovo", "armavir", "lobnya",
            "seversk", "mezhdurechensk", "kamenskuralsky", "miass", "elektrostal",
            "zlatoust", "serpukhov", "kopeyk", "almetyevsk", "odintsovo", "korolyov",
            "lyubertsy", "kovrov", "novouralsk", "khasavyurt", "pyatigorsk",
            "serov", "arzamas", "berezniki", "kislovodsk", "anapa", "gelendzhik",
            "yeysk", "komsomolsknaamure", "nizhnevartovsk", "novyurengoy",
            "magadan", "norilsk", "salekhard", "surgut", "khanty-mansiysk",
            "yuzhnosakhalinsk", "vorkuta", "nadym", "gubkinsky", "murmansk",
            "severomorsk", "arzamas", "arzamas", "ivanteevka"
        ]
        uuid = choice(cities)
        while f'{uuid}.json' in [file for file in listdir(path.join('saves', 'maps')) if file.endswith('.txt')]:
            uuid = choice(cities)

        return uuid

    def movement(self):
        """Логика передвижения.
        """
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

        if pg.key.get_pressed()[pg.K_ESCAPE]:
            self.selected_type_of_selector = (None, None)
            tile_selection: TileSelection = self.get_sprite('tile_selection')
            tile_selection.set_visible(False)

    def exit(self):
        """Остановка пингера при выходе.
        """
        self.game.pinger.running = False
