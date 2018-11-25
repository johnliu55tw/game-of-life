import logging

from game_of_life.presenter import GameOfLifePresenter


logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    g = GameOfLifePresenter(50, 50, 100)

    # Test
    g.world.set_alive(13, 13)
    g.world.set_alive(13, 14)
    g.world.set_alive(13, 15)
    g.world.set_alive(13, 16)
    g.world.set_alive(13, 17)
    g.world.set_alive(15, 13)
    g.world.set_alive(15, 17)
    g.world.set_alive(17, 13)
    g.world.set_alive(17, 14)
    g.world.set_alive(17, 15)
    g.world.set_alive(17, 16)
    g.world.set_alive(17, 17)

    g.run()
