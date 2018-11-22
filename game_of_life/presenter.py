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

        self.grid.bind('<Button-1>', self.on_left_click)

        # Test
        self.world.set_alive(13, 13)
        self.world.set_alive(13, 14)
        self.world.set_alive(13, 15)
        self.world.set_alive(13, 16)
        self.world.set_alive(13, 17)
        self.world.set_alive(15, 13)
        self.world.set_alive(15, 17)
        self.world.set_alive(17, 13)
        self.world.set_alive(17, 14)
        self.world.set_alive(17, 15)
        self.world.set_alive(17, 16)
        self.world.set_alive(17, 17)

    def start(self):
        self.root.after(self.delay, self.on_timer)
        self.root.mainloop()

    def on_timer(self):
        self.world.advance()
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if (x, y) in self.world.alives:
                    self.grid.set_alive(x, y)
                else:
                    self.grid.set_died(x, y)
        self.root.after(self.delay, self.on_timer)

    def on_left_click(self, event):
        logger.debug(f'Left click event: X: {event.x}, Y: {event.y}')
        cell = self.grid.get_cell_from_pixel_coor(event.x, event.y)
        if cell is not None:
            x, y = cell
            if (x, y) in self.world.alives:
                logger.debug(f'Set cell {x}, {y} to died.')
                self.world.set_dead(x, y)
                self.grid.set_died(x, y)
            else:
                logger.debug(f'Set cell {x}, {y} to alived.')
                self.world.set_alive(x, y)
                self.grid.set_alive(x, y)
        else:
            logger.debug(f'Left click: On border')
