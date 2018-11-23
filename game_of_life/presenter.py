import logging
import tkinter

from .view import Grid
from .model import World


logger = logging.getLogger(__name__)


class GameOfLifePresenter(object):

    def __init__(self, width, height, delay):
        self.size = (width, height)
        self.delay = delay

        self.root = tkinter.Tk()
        self.grid = Grid(width, height)
        self.world = World(width, height)

        self.grid.bind('<<Cell-Click>>', self.on_cell_click)

    def start(self):
        self.root.after(self.delay, self.on_timer)
        self.root.mainloop()

    def on_timer(self):
        self.world.advance()
        self.grid.set_alives(self.world.alives)
        self.root.after(self.delay, self.on_timer)

    def on_cell_click(self, event):
        logger.debug('on_cell_click! X:{}, Y:{}'.format(event.x, event.y))
        x, y = event.x, event.y

        if (x, y) in self.world.alives:
            logger.debug('Set cell {}, {} to dead.'.format(x, y))
            self.world.set_dead(x, y)
        else:
            logger.debug('Set cell {}, {} to alive.'.format(x, y))
            self.world.set_alive(x, y)

        self.grid.set_alives(self.world.alives)
