"""
Void Hunter - 2D Space Shooter
Точка входа в игру
"""

from src.game import Game


def main():
    """Запуск игры"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
