import logging
import tkinter

from .view import MainView
from .model import World, Patterns


logger = logging.getLogger(__name__)


class GameOfLifePresenter(object):

    def __init__(self, width, height, min_delay):
        self.root = tkinter.Tk()
        self.main_view = MainView(width, height,
                                  pattern_options=[p.name for p in Patterns],
                                  master=self.root)
        self.world = World(width, height)

        default_pattern = Patterns[0]
        for x, y in default_pattern.as_screen_coordinate(width, height):
            self.world.set_alive(x, y)

        self.size = (width, height)
        self.min_delay = min_delay
        self._timer_delay = None
        # Initial speed. Don't change it or the speed will differ from the speed
        # scroller!
        self.set_speed(0.1)
        self.stop()

        # Must use bind_all to capture event
        self.main_view.bind_all('<<Cell-Click>>', self.on_cell_click)
        self.main_view.bind_all('<<StartStop-Toggle>>', self.on_startstop_toggle)
        self.main_view.bind_all('<<Next-Click>>', self.on_next_click)
        self.main_view.bind_all('<<Speed-Change>>', self.on_speed_change)
        self.main_view.bind_all('<<PatternOption-Change>>', self.on_pattern_option_change)

    @property
    def is_running(self):
        return self._is_running

    def run(self):
        self.main_view.update(alives=self.world.alives)
        self.stop()
        self.root.mainloop()

    def start(self):
        self._is_running = True
        self.main_view.update(startstop_text='Stop')
        self.root.after(self._timer_delay, self.on_timer)

    def stop(self):
        self._is_running = False
        self.main_view.update(startstop_text='Start')

    def set_speed(self, scale):
        if scale <= 0 or scale > 1:
            raise ValueError('Speed must be within 0 < scale <= 1')

        new_delay = int(self.min_delay / scale)
        logger.debug('Change delay to {}'.format(new_delay))
        self._timer_delay = new_delay

    def on_timer(self):
        if self._is_running:
            self.world.advance()
            self.main_view.update(alives=self.world.alives)
            self.root.after(self._timer_delay, self.on_timer)

    def on_cell_click(self, event):
        logger.debug('on_cell_click! X:{}, Y:{}'.format(event.x, event.y))
        x, y = event.x, event.y

        self.world.toggle_aliveness(x, y)
        self.main_view.update(alives=self.world.alives)

    def on_startstop_toggle(self, event):
        logger.debug('StartStop Toggled!')
        if self._is_running:
            self.stop()
        else:
            self.start()

    def on_next_click(self, event):
        self.world.advance()
        self.main_view.update(alives=self.world.alives)

    def on_speed_change(self, event):
        logger.debug('Speed change event: {}'.format(event.x))
        self.set_speed(event.x/100)

    def on_pattern_option_change(self, event):
        logger.debug('Option Menu change, index: {}'.format(event.x))
        pattern = Patterns[event.x]

        self.world = World(self.size[0], self.size[1])
        for alive_cell in pattern.as_screen_coordinate(self.size[0], self.size[1]):
            self.world.set_alive(alive_cell[0], alive_cell[1])

        self.main_view.update(alives=self.world.alives)
