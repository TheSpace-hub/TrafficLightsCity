from typing import TYPE_CHECKING

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
            field.camera_distance -= .1
            field.update_view()
        elif 4 in self.game.omitted_mouse_buttons:
            field: Field = self.get_sprite('field')
            field.camera_distance += .1
            field.update_view()

    def enter(self):
        pass

    def exit(self):
        pass
