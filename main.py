"""
Основной файл программы
"""
from src.game import Game


def main():
    """
    Функция запускает при запуске программы
    """
    Game().loop()


if __name__ == '__main__':
    main()
