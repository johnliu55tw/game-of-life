import logging
import tkinter

from .view import MainView
from .model import World


logger = logging.getLogger(__name__)


class GameOfLifePresenter(object):

    def __init__(self, width, height, delay):
        self.size = (width, height)
        self.delay = delay
        self._is_running = False

        self.root = tkinter.Tk()
        self.main_view = MainView(width, height, master=self.root)
        self.world = World(width, height)

        # Must use bind_all to capture event
        self.main_view.bind_all('<<Cell-Click>>', self.on_cell_click)
        self.main_view.bind_all('<<StartStop-Toggle>>', self.on_startstop_toggle)

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
        self.root.after(self.delay, self.on_timer)

    def stop(self):
        self._is_running = False
        self.main_view.update(startstop_text='Start')

    def on_timer(self):
        if self._is_running:
            self.world.advance()
            self.main_view.update(alives=self.world.alives)
            self.root.after(self.delay, self.on_timer)

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
