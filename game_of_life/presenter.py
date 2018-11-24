import logging
import tkinter

from .view import Grid
from .model import World


logger = logging.getLogger(__name__)


class GameOfLifePresenter(object):

    def __init__(self, width, height, delay):
        self.size = (width, height)
        self.delay = delay
        self._is_running = False

        self.root = tkinter.Tk()
        self.grid = Grid(width, height)
        self.world = World(width, height)

        self.grid.bind('<<Cell-Click>>', self.on_cell_click)

    @property
    def is_running(self):
        return self._is_running

    def start(self):
        self._is_running = True
        self.root.after(self.delay, self.on_timer)
        self.root.mainloop()

    def stop(self):
        self._is_running = False

    def on_timer(self):
        if self._is_running:
            self.world.advance()
            self.grid.set_alives(self.world.alives)
            self.root.after(self.delay, self.on_timer)

    def on_cell_click(self, event):
        logger.debug('on_cell_click! X:{}, Y:{}'.format(event.x, event.y))
        x, y = event.x, event.y

        self.world.toggle_aliveness(x, y)
        self.grid.set_alives(self.world.alives)
