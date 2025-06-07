"""
Основной файл программы
"""
from src.game import Game


def main():
    """
    Функция запускает при запуске программы
    """
    game = Game()
    game.change_state('Intro')
    game.loop()


if __name__ == '__main__':
    main()
