from tkinter import Frame

from .view import Grid
from .model import World


class GameOfLifePresenter(Frame):

    def __init__(self, width, height, delay, master=None):
        if master is not None:
            super().__init__(master)
        self.size = (width, height)
        self.delay = delay
        self.grid = Grid(width, height)
        self.world = World(width, height)

        self.after(self.delay, self.on_timer)
        self.pack()
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

    def on_timer(self):
        self.world.advance()
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if (x, y) in self.world.alives:
                    self.grid.set_alive(x, y)
                else:
                    self.grid.set_died(x, y)
        self.after(self.delay, self.on_timer)
