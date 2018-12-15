import logging
from functools import partial
from tkinter import Canvas, Frame, Button, Scale, OptionMenu
from tkinter import StringVar
from tkinter import HORIZONTAL, END


logger = logging.getLogger(__name__)


class Grid(Canvas):
    CELL_SIZE = 15  # pixel
    OUTLINE_WIDTH = 1  # pixel
    OUTLINE_COLOR = 'black'
    ALIVE_COLOR = 'yellow'
    DEAD_COLOR = 'grey'

    def __init__(self, width, height, master=None):
        self._master = master

        self.width = width
        self.height = height
        self._alive_cells = frozenset()

        w_px = (self.CELL_SIZE + self.OUTLINE_WIDTH) * width + self.OUTLINE_WIDTH
        h_px = (self.CELL_SIZE + self.OUTLINE_WIDTH) * height + self.OUTLINE_WIDTH
        super().__init__(width=w_px,
                         height=h_px,
                         borderwidth=0,
                         background=self.OUTLINE_COLOR,
                         highlightthickness=0,
                         master=self._master)
        self._cells = self._init_cells()

        self.bind('<Button-1>', self._translate_click_event)

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
            # XXX: Noted that I this line changed the meaning of "x" and "y"
            # attributes of an event. Since there's no other way to pass
            # customize data, this is the best I could do.
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

    def _set_alive(self, cell_x, cell_y):
        self.itemconfig(self._cells[cell_x][cell_y], fill=self.ALIVE_COLOR)

    def _set_dead(self, cell_x, cell_y):
        self.itemconfig(self._cells[cell_x][cell_y], fill=self.DEAD_COLOR)

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


class StartStopButton(Button):

    def __init__(self, master=None):
        self._master = master
        super().__init__(text='Start',
                         width=10,
                         master=self._master,
                         command=self._translate_click_event)

    def _translate_click_event(self):
        logger.debug('StartStopButton <Button-1> received. Translating into <<StartStop-Toggle>>')
        self.event_generate('<<StartStop-Toggle>>')


class NextButton(Button):

    def __init__(self, master=None):
        self._master = master
        super().__init__(text='Next',
                         width=10,
                         master=self._master,
                         command=self._translate_click_event)

    def _translate_click_event(self):
        logger.debug('NextButton <Button-1> received. Translating into <<Next-Click>>')
        self.event_generate('<<Next-Click>>')


class SpeedSlider(Scale):

    def __init__(self, master=None):
        self._master = master
        super().__init__(from_=10,
                         to=100,
                         resolution=10,
                         orient=HORIZONTAL,
                         master=self._master,
                         showvalue=0,
                         command=self._translate_click_event)

    def _translate_click_event(self, value):
        logger.debug('SpeedSlider value {} received.'
                     ' Translating into <<Speed-Change>>.'.format(value))
        # XXX: I use attribute "x" to carry the value information.
        # Also, it must be an int :(
        self.event_generate('<<Speed-Change>>', x=value)


class PatternOptionMenu(OptionMenu):

    def __init__(self, master=None, options=None, default_index=0):
        self._master = master
        self._var = StringVar()
        self._var.set('')

        super().__init__(self._master,
                         self._var,
                         '')

        if options is not None:
            self.update_options(options, default_index=default_index)

    def update_options(self, options, default_index=0):
        # Updating the menu is done by manipulating the internal "Menu" object.
        menu_obj = self['menu']
        menu_obj.delete(0, END)
        for i, option in enumerate(options):
            menu_obj.add_command(label=option,
                                 command=partial(self._on_selection_changed,
                                                 index=i,
                                                 option=option))
        # XXX: This Control Variable is still needed to show the selected
        # value on the button.
        self._var.set(options[default_index])

    def _on_selection_changed(self, index, option):
        logger.debug('selection changed to {}:{}'.format(index, option))
        self._var.set(option)
        self.event_generate('<<PatternOption-Change>>', x=index)


class MainView(Frame):

    def __init__(self, grid_width, grid_height, pattern_options, master=None):
        self._master = master
        super().__init__(bg='white',
                         master=self._master)

        self.world_grid = Grid(width=grid_width, height=grid_height, master=self)
        self.startstop_button = StartStopButton(master=self)
        self.next_button = NextButton(master=self)
        self.speed_slider = SpeedSlider(master=self)
        self.pattern_option_menu = PatternOptionMenu(master=self,
                                                     options=pattern_options)

        self.world_grid.grid(row=0, column=0, columnspan=4)
        self.startstop_button.grid(row=1, column=0, pady=5, padx=5)
        self.next_button.grid(row=1, column=1, pady=5, padx=5)
        self.speed_slider.grid(row=1, column=2, pady=5, padx=5)
        self.pattern_option_menu.grid(row=1, column=3, pady=5, padx=5)

        self.pack()

    def update(self, alives=None, startstop_text=None, pattern_options=None):
        if alives is not None:
            self.world_grid.set_alives(alives)
        if startstop_text is not None:
            self.startstop_button.config(text=startstop_text)
        if pattern_options is not None:
            self.pattern_option_menus.update_options(pattern_options)
