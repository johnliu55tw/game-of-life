from unittest import TestCase, mock

from game_of_life import presenter


@mock.patch('game_of_life.presenter.tkinter')
@mock.patch('game_of_life.presenter.MainView')
@mock.patch('game_of_life.presenter.World')
class GameOfLifePresenterTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_constructor(self, m_world, m_main_view, m_tkinter):
        p = presenter.GameOfLifePresenter(5, 6, 123)

        self.assertIsInstance(p, presenter.GameOfLifePresenter)
        self.assertEqual(p.size, (5, 6))
        self.assertEqual(p.min_delay, 123)
        self.assertEqual(p.is_running, False)
        self.assertEqual(p.main_view, m_main_view.return_value)
        self.assertEqual(p.world, m_world.return_value)
        self.assertEqual(p.root, m_tkinter.Tk.return_value)

        p.main_view.bind_all.assert_has_calls([
            mock.call('<<Cell-Click>>', p.on_cell_click),
            mock.call('<<StartStop-Toggle>>', p.on_startstop_toggle),
            mock.call('<<Next-Click>>', p.on_next_click),
            mock.call('<<Speed-Change>>', p.on_speed_change),
        ])

    def test_is_running_property(self, m_world, m_main_view, m_tkinter):
        p = presenter.GameOfLifePresenter(5, 6, 123)

        self.assertEqual(p.is_running, False)
        with self.assertRaises(AttributeError):
            p.is_running = True

    def test_run(self, m_world, m_main_view, m_tkinter):
        root_inst = mock.Mock()
        m_tkinter.Tk.return_value = root_inst
        main_view_inst = m_main_view.return_value
        world_inst = m_world.return_value
        p = presenter.GameOfLifePresenter(5, 6, 123)

        with mock.patch.object(p, 'stop'):
            p.run()

            p.stop.assert_called()
            main_view_inst.update.assert_called_with(alives=world_inst.alives)
            root_inst.mainloop.assert_called()

    def test_start(self, m_world, m_main_view, m_tkinter):
        root_inst = mock.Mock()
        m_tkinter.Tk.return_value = root_inst
        main_view_inst = m_main_view.return_value
        p = presenter.GameOfLifePresenter(5, 6, 123)
        p.run()

        p.start()

        root_inst.after.assert_called_with(p._timer_delay, p.on_timer)
        self.assertTrue(p.is_running)
        main_view_inst.update.assert_called_with(startstop_text='Stop')

    def test_stop(self, m_world, m_main_view, m_tkinter):
        main_view_inst = m_main_view.return_value
        p = presenter.GameOfLifePresenter(5, 6, 123)
        p.run()

        p.stop()

        self.assertFalse(p.is_running)
        main_view_inst.update.assert_called_with(startstop_text='Start')

    def test_set_speed(self, m_world, m_main_view, m_tkinter):
        p = presenter.GameOfLifePresenter(5, 6, 123)
        p.run()

        p.set_speed(0.1)
        self.assertEqual(p._timer_delay, int(123/0.1))

        p.set_speed(0.5)
        self.assertEqual(p._timer_delay, int(123/0.5))

        p.set_speed(1)
        self.assertEqual(p._timer_delay, int(123/1))

    def test_set_speed_out_of_bound(self, m_world, m_main_view, m_tkinter):
        p = presenter.GameOfLifePresenter(5, 6, 123)
        p.run()

        with self.assertRaises(ValueError):
            p.set_speed(0)

        with self.assertRaises(ValueError):
            p.set_speed(1.0001)

        with self.assertRaises(ValueError):
            p.set_speed(-0.001)

    def test_on_timer_when_is_running(self, m_world, m_main_view, m_tkinter):
        p = presenter.GameOfLifePresenter(5, 6, 123)
        p.run()
        p.start()

        p.on_timer()

        world_inst = m_world.return_value
        main_view_inst = m_main_view.return_value
        root_inst = m_tkinter.Tk.return_value

        world_inst.advance.assert_called()
        main_view_inst.update.assert_called_with(alives=world_inst.alives)
        root_inst.after.assert_called_with(p._timer_delay, p.on_timer)

    def test_on_timer_when_not_is_running(self, m_world, m_main_view, m_tkinter):
        p = presenter.GameOfLifePresenter(5, 6, 123)
        p.run()

        p.on_timer()

        world_inst = m_world.return_value
        main_view_inst = m_main_view.return_value
        root_inst = m_tkinter.Tk.return_value

        world_inst.advance.assert_not_called()
        main_view_inst.set_alives.assert_not_called()
        root_inst.after.assert_not_called()

    def test_on_cell_click(self, m_world, m_main_view, m_tkinter):
        p = presenter.GameOfLifePresenter(5, 6, 123)
        p.run()
        fake_event = mock.Mock()
        fake_event.x = 2
        fake_event.y = 3

        p.on_cell_click(fake_event)

        world_inst = m_world.return_value
        main_view_inst = m_main_view.return_value

        world_inst.toggle_aliveness.assert_called_with(fake_event.x, fake_event.y)
        main_view_inst.update.assert_called_with(alives=world_inst.alives)

    def test_on_startstop_toggle_when_is_running(self, m_world, m_main_view, m_tkinter):
        p = presenter.GameOfLifePresenter(5, 6, 123)
        p.run()
        p.start()

        with mock.patch.object(p, 'stop'):
            p.on_startstop_toggle(mock.Mock())
            p.stop.assert_called()

    def test_on_startstop_toggle_when_not_running(self, m_world, m_main_view, m_tkinter):
        p = presenter.GameOfLifePresenter(5, 6, 123)
        p.run()
        p.start()
        p.stop()

        with mock.patch.object(p, 'start'):
            p.on_startstop_toggle(mock.Mock())
            p.start.assert_called()

    def test_on_next_click_when_is_running(self, m_world, m_main_view, m_tkinter):
        p = presenter.GameOfLifePresenter(5, 6, 123)
        p.run()
        p.start()
        # Reset them to verify the behavior of the target function
        p.world.reset_mock()
        p.main_view.reset_mock()

        p.on_next_click(mock.Mock())

        p.world.advance.assert_called()
        p.main_view.update.assert_called_with(alives=p.world.alives)

    def test_on_speed_change(self, m_world, m_main_view, m_tkinter):
        p = presenter.GameOfLifePresenter(5, 6, 123)
        p.run()
        p.start()
        fake_event = mock.Mock()
        fake_event.x = 30

        with mock.patch.object(p, 'set_speed'):
            p.on_speed_change(fake_event)
            p.set_speed.assert_called_with(0.3)
