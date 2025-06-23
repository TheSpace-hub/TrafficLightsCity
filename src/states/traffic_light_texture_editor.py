from typing import TYPE_CHECKING
from tkinter import filedialog
from PIL import Image
import numpy as np

from src.state import State

from src.sprites import Pixelart, Button, InBlockText, ButtonStatus

if TYPE_CHECKING:
    from src.game import Game


class TrafficLightTextureEditor(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.images: dict[str, str] = {}
        self.current_pixelart: int = 0

    def boot(self):
        self.add_sprite('add_texture_button', Button(self.game, 100, 50, 400, 70,
                                                     InBlockText(self.game, 'Добавить изображение', 16,
                                                                 (255, 255, 255)), self.on_create_world_button_pressed))

    def on_create_world_button_pressed(self, status: ButtonStatus):
        if status == ButtonStatus.PRESSED:
            file_path: str = filedialog.askopenfilename(
                title="Выберите изображение",
                filetypes=[("Изображение секции светофора", "*.png"), ("Любой файл", "*.*")]
            )
            image: Image = Image.open(file_path).convert('RGBA')
            image_name: str = file_path.split('/')[-1:][0].split('.')[0].lower()
            pixel_rows = [
                tuple(list(image.getdata())[i * image.size[0]: (i + 1) * image.size[0]])
                for i in range(image.size[1])
            ]
            self.add_sprite('pixelart_1',
                            Pixelart(self.game, (110, 150), 10, tuple(tuple(row) for row in pixel_rows)))
            self.images['pixelart_new'] = image_name

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass
