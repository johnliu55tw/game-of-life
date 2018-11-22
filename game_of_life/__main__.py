import logging

from game_of_life.presenter import GameOfLifePresenter


logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    g = GameOfLifePresenter(50, 50, 100)
    g.start()
