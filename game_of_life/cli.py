import logging

from game_of_life.presenter import GameOfLifePresenter


logging.basicConfig(level=logging.DEBUG)


def main():
    g = GameOfLifePresenter(50, 50, 50)
    g.run()
