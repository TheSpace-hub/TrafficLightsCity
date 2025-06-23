from typing import TYPE_CHECKING
from tkinter import filedialog

from src.state import State

from src.sprites import Pixelart, Button, InBlockText, ButtonStatus, Container, Input, Formatting

if TYPE_CHECKING:
    from src.game import Game


class TrafficLightTextureEditor(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.images: dict[str, str] = {}
        self.current_container: int = 0

    def boot(self):
        self.add_sprite('texture_name_input', Input(self.game, 100, 50, 700, 70,
                                                    InBlockText(self.game, '', 16, (255, 255, 255)),
                                                    InBlockText(self.game, 'Введите название текстуры', 16,
                                                                (255, 255, 255)),
                                                    Formatting.NORMALIZED
                                                    ))
        self.add_sprite('add_texture_button', Button(self.game, 100, 130, 400, 70,
                                                     InBlockText(self.game, 'Добавить изображение', 16,
                                                                 (255, 255, 255)), self.on_create_world_button_pressed))
        self.add_sprite('create_texture_button', Button(self.game, 510, 130, 400, 70,
                                                        InBlockText(self.game, 'Создать текстуру', 16,
                                                                    (255, 255, 255)),
                                                        self.on_create_world_button_pressed,
                                                        False))

    def on_create_world_button_pressed(self, status: ButtonStatus):
        if status == ButtonStatus.PRESSED:
            file_path: str = filedialog.askopenfilename(
                title="Выберите изображение",
                filetypes=[("Изображение секции светофора", "*.png"), ("Любой файл", "*.*")]
            )
            image_name: str = file_path.split('/')[-1:][0].split('.')[0].lower()
            self.add_sprite(f'container_pixelart_{self.current_container}',
                            Container(self.game, (100, 210 + 110 * self.current_container), (500, 100)))
            self.add_sprite(f'pixelart_{self.current_container}',
                            Pixelart(self.game, (110, 220 + 110 * self.current_container), (80, 80),
                                     Pixelart.get_pixelart_by_image(file_path)))
            self.add_sprite(f'pixelart_name_input_{self.current_container}',
                            Input(self.game, 200, 225 + 110 * self.current_container, 380, 70,
                                  InBlockText(self.game, image_name, 16, (255, 255, 255)),
                                  InBlockText(self.game, 'Введите название', 16, (255, 255, 255)),
                                  Formatting.NORMALIZED
                                  ))
            self.images['pixelart_new'] = image_name
            self.current_container += 1

    def update(self):
        texture_name_input: Input = self.get_sprite('texture_name_input')
        create_texture_button: Button = self.get_sprite('create_texture_button')
        create_texture_button.enabled = self.current_container > 0 and texture_name_input.text.text != ''

    def enter(self):
        pass

    def exit(self):
        pass
