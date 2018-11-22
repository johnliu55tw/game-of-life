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
        super().__init__(width=w_px,
                         height=h_px,
                         borderwidth=0,
                         background=self.OUTLINE_COLOR,
                         highlightthickness=0)
        self._cells = self._init_cells()
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

    def get_cell_from_pixel_coor(self, px_x, px_y):
        cell_size = self.CELL_SIZE + self.OUTLINE_WIDTH
        cell_x = int(px_x / cell_size)
        remainder_x = px_x % cell_size
        if remainder_x <= self.OUTLINE_WIDTH:
            return None

        cell_y = int(px_y / cell_size)
        cell_y = int(px_y / cell_size)
        remainder_y = px_y % cell_size
        if remainder_y <= self.OUTLINE_WIDTH:
            return None

        return (cell_x, cell_y)