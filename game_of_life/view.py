import logging
from tkinter import Canvas


logger = logging.getLogger(__name__)


class Grid(Canvas):
    CELL_SIZE = 15  # pixel
    OUTLINE_WIDTH = 1  # pixel
    OUTLINE_COLOR = 'black'
    ALIVE_COLOR = 'yellow'
    DEAD_COLOR = 'grey'

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._alive_cells = frozenset()

        w_px = (self.CELL_SIZE + self.OUTLINE_WIDTH) * width + self.OUTLINE_WIDTH
        h_px = (self.CELL_SIZE + self.OUTLINE_WIDTH) * height + self.OUTLINE_WIDTH
        super().__init__(width=w_px,
                         height=h_px,
                         borderwidth=0,
                         background=self.OUTLINE_COLOR,
                         highlightthickness=0)
        self._cells = self._init_cells()

        self.bind('<Button-1>', self._translate_click_event)

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
                                          width=0, fill=self.DEAD_COLOR)
                ys.append(r)
        return cells

    def _translate_click_event(self, event):
        logger.debug('<Button-1> event received. Translating into <<Cell-Click>>.')
        cell = self._get_cell_from_pixel_coor(event.x, event.y)
        if cell is not None:
            x, y = cell
            self.event_generate('<<Cell-Click>>', x=x, y=y)

    def _get_cell_from_pixel_coor(self, px_x, px_y):
        cell_size = self.CELL_SIZE + self.OUTLINE_WIDTH
        cell_x = int(px_x / cell_size)
        remainder_x = px_x % cell_size
        if remainder_x <= self.OUTLINE_WIDTH:
            # Click on outline does not count.
            return None

        cell_y = int(px_y / cell_size)
        cell_y = int(px_y / cell_size)
        remainder_y = px_y % cell_size
        if remainder_y <= self.OUTLINE_WIDTH:
            # Click on outline does not count.
            return None

        return (cell_x, cell_y)

    def _set_alive(self, x, y):
        self.itemconfig(self._cells[x][y], fill=self.ALIVE_COLOR)

    def _set_dead(self, x, y):
        self.itemconfig(self._cells[x][y], fill=self.DEAD_COLOR)

    def set_alives(self, alive_cells):
        alive_cells = frozenset(alive_cells)

        # Calculate the changes from current alive cells to the new alive cells
        now_dead_cells = self._alive_cells - alive_cells
        now_alive_cells = alive_cells - self._alive_cells

        # Update cell state
        for x, y in now_dead_cells:
            self._set_dead(x, y)
        for x, y in now_alive_cells:
            self._set_alive(x, y)

        self._alive_cells = alive_cells
