import logging
from tkinter import Canvas


logger = logging.getLogger(__name__)


class Grid(Canvas):
    CELL_SIZE = 15  # pixel
    OUTLINE_WIDTH = 1  # pixel
    OUTLINE_COLOR = 'black'
    ALIVE_COLOR = 'yellow'
    DIED_COLOR = 'grey'

    def __init__(self, width, height):
        self.width = width
        self.height = height

        w_px = (self.CELL_SIZE + self.OUTLINE_WIDTH) * width + self.OUTLINE_WIDTH
        h_px = (self.CELL_SIZE + self.OUTLINE_WIDTH) * height + self.OUTLINE_WIDTH
        logger.debug('width px: {}, height_px: {}'.format(w_px, h_px))
        super().__init__(width=w_px,
                         height=h_px,
                         borderwidth=0,
                         background=self.OUTLINE_COLOR,
                         highlightthickness=0)
        self._cells = self._init_cells()
        self.test_flag = True
        self.pack()

    def _gen_coors(self, n):
        space = self.CELL_SIZE + self.OUTLINE_WIDTH
        for i in range(n):
            yield i * space + self.OUTLINE_WIDTH

    def _init_cells(self):
        cells = list()

        for x in self._gen_coors(self.width):
            ys = list()
            cells.append(ys)
            for y in self._gen_coors(self.height):
                r = self.create_rectangle(x, y,
                                          x+self.CELL_SIZE, y+self.CELL_SIZE,
                                          width=0, fill=self.DIED_COLOR)
                ys.append(r)
        return cells

    def set_alive(self, x, y):
        self.itemconfig(self._cells[x][y], fill=self.ALIVE_COLOR)

    def set_died(self, x, y):
        self.itemconfig(self._cells[x][y], fill=self.DIED_COLOR)
