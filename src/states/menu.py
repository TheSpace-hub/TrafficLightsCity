from typing import TYPE_CHECKING

from src.state import State

from src.sprites import Button, InButtonText

if TYPE_CHECKING:
    from src.game import Game



class Menu(State):
    def __init__(self, game: 'Game'):
        super().__init__(game)

    def boot(self):
        self.add_sprite('create_city', Button(self.game, 510, 460, 900, 70,
                                           InButtonText(self.game, 'Создать город', 16,
                                                        (255, 255, 255))))
        self.add_sprite('open_city', Button(self.game, 510, 540, 900, 70,
                                           InButtonText(self.game, 'Открыть город', 16,
                                                        (255, 255, 255))))
        self.add_sprite('settings', Button(self.game, 510, 620, 900, 70,
                                           InButtonText(self.game, 'Настройки', 16,
                                                        (255, 255, 255))))

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass
