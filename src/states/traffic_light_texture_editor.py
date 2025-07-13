from typing import TYPE_CHECKING, Literal
from tkinter import filedialog
from os import path
import json

from src.state import State

from src.sprites import Pixelart, Button, InBlockText, ButtonStatus, Container, Input, Formatting, Text, TextAlign

if TYPE_CHECKING:
    from src.game import Game


class TrafficLightTextureEditor(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.images: dict[str, str] = {}
        self.current_container: int = 0

    def boot(self):
        self.add_sprite('back', Button(self.game, (1710, 1000), (200, 70),
                                       InBlockText(self.game, 'Назад', 16,
                                                   (255, 255, 255)),
                                       self.on_back_button_pressed))
        self.add_sprite('texture_name_input', Input(self.game, (100, 50), (700, 70),
                                                    InBlockText(self.game, '', 16, (255, 255, 255)),
                                                    InBlockText(self.game, 'Введите ID текстуры', 16,
                                                                (128, 128, 128)),
                                                    Formatting.NORMALIZED
                                                    ))
        self.add_sprite('add_image_button', Button(self.game, (100, 130), (400, 70),
                                                   InBlockText(self.game, 'Добавить изображение', 16,
                                                               (255, 255, 255)), self.on_add_image_button_pressed))
        self.add_sprite('create_texture_button', Button(self.game, (510, 130), (400, 70),
                                                        InBlockText(self.game, 'Создать текстуру', 16,
                                                                    (255, 255, 255)),
                                                        self.on_create_texture_button_pressed, enabled=False))
        self.add_sprite('create_texture_info', Text(self.game, (610, 205), '',
                                                    13, (0, 255, 0), align=TextAlign.LEFT))

    def on_add_image_button_pressed(self, status: ButtonStatus):
        if status == ButtonStatus.PRESSED:
            file_paths: Literal[""] | tuple[str, ...] = filedialog.askopenfilenames(
                title="Выберите изображение",
                filetypes=[("Изображение секции светофора", "*.png"), ("Любой файл", "*.*")]
            )
            if file_paths == ():
                return
            for file_path in file_paths:
                image_name: str = file_path.split('/')[-1:][0].split('.')[0].lower()
                self.add_sprite(f'container_pixelart_{self.current_container}',
                                Container(self.game, (100, 210 + 110 * self.current_container), (500, 100)))
                self.add_sprite(f'pixelart_{self.current_container}',
                                Pixelart(self.game, (110, 220 + 110 * self.current_container), (80, 80),
                                         Pixelart.get_pixelart_by_image(file_path)))
                self.add_sprite(f'pixelart_name_input_{self.current_container}',
                                Input(self.game, (200, 225 + 110 * self.current_container), (380, 70),
                                      InBlockText(self.game, image_name, 16, (255, 255, 255)),
                                      InBlockText(self.game, 'Введите ID картинки', 16, (128, 128, 128)),
                                      Formatting.NORMALIZED
                                      ))
                self.images['pixelart_new'] = image_name
                self.current_container += 1

    def on_create_texture_button_pressed(self, status: ButtonStatus):
        if status != ButtonStatus.PRESSED:
            return
        texture_name: str = self.get_sprite('texture_name_input').text.text
        texture: dict = {}
        for i in range(self.current_container):
            pixelart_name_input: Input = self.get_sprite(f'pixelart_name_input_{i}')
            pixelart: Pixelart = self.get_sprite(f'pixelart_{i}')
            texture[pixelart_name_input.text.text] = pixelart.pixelart

        with open(path.join('saves', 'traffic_lights', 'textures', f'{texture_name}.json'), 'w') as file:
            file.write(json.dumps(texture))

        create_texture_info: Text = self.get_sprite('create_texture_info')
        create_texture_info.text = 'Текстура создана'
        create_texture_info.update_view()

    def update(self):
        create_texture_button: Button = self.get_sprite('create_texture_button')
        create_texture_button.enabled = self.is_it_possible_to_create_texture()

    def is_it_possible_to_create_texture(self) -> bool:
        texture_name_input: Input = self.get_sprite('texture_name_input')

        used_ids: list[str] = []
        for i in range(self.current_container):
            pixelart_name_input: Input = self.get_sprite(f'pixelart_name_input_{i}')
            if pixelart_name_input.text.text == '' or pixelart_name_input.text.text in used_ids:
                return False
            used_ids.append(pixelart_name_input.text.text)
        return self.current_container > 0 and texture_name_input.text.text != ''

    def on_back_button_pressed(self, status: ButtonStatus):
        if status == ButtonStatus.PRESSED:
            self.images: dict[str, str] = {}
            self.current_container: int = 0
            for uuid, sprite in self.get_sprites().copy().items():
                if 'pixelart' in uuid:
                    self.remove_sprite(uuid)
            self.game.change_state('Menu')

    def enter(self):
        pass

    def exit(self):
        pass
