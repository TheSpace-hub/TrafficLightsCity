from typing import TYPE_CHECKING

from src.state import State

from src.sprites import Button, InBlockText, ButtonStatus

if TYPE_CHECKING:
    from src.game import Game


class Menu(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)

    def boot(self):
        self.add_sprite('create_city', Button(self.game, (510, 460), (900, 70),
                                              InBlockText(self.game, 'Создать город', 16,
                                                          (255, 255, 255)),
                                              self.on_create_city_button_pressed))
        self.add_sprite('open_city', Button(self.game, (510, 540), (900, 70),
                                            InBlockText(self.game, 'Открыть город', 16,
                                                        (255, 255, 255)),
                                            self.on_open_city_button_pressed))
        self.add_sprite('traffic_light_editor', Button(self.game, (510, 620), (445, 70),
                                                       InBlockText(self.game, 'Редактор светофоров', 16,
                                                                   (255, 255, 255)),
                                                       enabled=False))
        self.add_sprite('traffic_light_texture_editor', Button(self.game, (965, 620), (445, 70),
                                                               InBlockText(self.game, 'Редактор текстур', 16,
                                                                           (255, 255, 255)),
                                                               self.on_traffic_light_texture_editor_button_pressed))
        self.add_sprite('settings', Button(self.game, (510, 700), (445, 70),
                                           InBlockText(self.game, 'Настройки', 16,
                                                       (255, 255, 255)),
                                           self.on_settings_button_pressed))
        self.add_sprite('quit', Button(self.game, (965, 700), (445, 70),
                                       InBlockText(self.game, 'Выход', 16,
                                                   (255, 255, 255)),
                                       self.on_quit_button_pressed))

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass

    def on_create_city_button_pressed(self, status: ButtonStatus):
        if status == ButtonStatus.PRESSED:
            self.game.change_state('CreateCity')

    def on_settings_button_pressed(self, status: ButtonStatus):
        if status == ButtonStatus.PRESSED:
            self.game.change_state('Settings')

    def on_traffic_light_texture_editor_button_pressed(self, status: ButtonStatus):
        if status == ButtonStatus.PRESSED:
            self.game.change_state('TrafficLightTextureEditor')

    def on_quit_button_pressed(self, status: ButtonStatus):
        if status == ButtonStatus.PRESSED:
            self.game.quit()

    def on_open_city_button_pressed(self, status: ButtonStatus):
        if status == ButtonStatus.PRESSED:
            self.game.change_state('OpenCity')
