from typing import TYPE_CHECKING
from tkinter import filedialog

from src.state import State

from src.sprites import Pixelart, Button, InBlockText, ButtonStatus, Container

if TYPE_CHECKING:
    from src.game import Game


class TrafficLightTextureEditor(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.images: dict[str, str] = {}
        self.current_container: int = 0

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
            image_name: str = file_path.split('/')[-1:][0].split('.')[0].lower()
            self.add_sprite(f'container_pixelart_{self.current_container}',
                            Container(self.game, (100, 150), (1000, 300)))
            self.add_sprite(f'pixelart_{self.current_container}',
                            Pixelart(self.game, (100, 150), (300, 300), Pixelart.get_pixelart_by_image(file_path)))
            self.images['pixelart_new'] = image_name
            self.current_container += 1

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass
