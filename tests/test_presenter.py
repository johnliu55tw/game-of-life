from unittest import TestCase, mock

from game_of_life import presenter


@mock.patch('game_of_life.presenter.tkinter')
@mock.patch('game_of_life.presenter.Grid')
@mock.patch('game_of_life.presenter.World')
class GameOfLifePresenterTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_constructor(self, m_world, m_grid, m_tkinter):
        p = presenter.GameOfLifePresenter(5, 6, 123)

        self.assertIsInstance(p, presenter.GameOfLifePresenter)
        self.assertEqual(p.size, (5, 6))
        self.assertEqual(p.delay, 123)
        self.assertEqual(p.is_running, False)
        self.assertEqual(p.grid, m_grid.return_value)
        self.assertEqual(p.world, m_world.return_value)
        self.assertEqual(p.root, m_tkinter.Tk.return_value)

    def test_is_running_property(self, m_world, m_grid, m_tkinter):
        p = presenter.GameOfLifePresenter(5, 6, 123)

        self.assertEqual(p.is_running, False)
        with self.assertRaises(AttributeError):
            p.is_running = True

    def test_start(self, m_world, m_grid, m_tkinter):
        root_inst = mock.Mock()
        m_tkinter.Tk.return_value = root_inst

        p = presenter.GameOfLifePresenter(5, 6, 123)
        p.start()

        root_inst.after.assert_called_with(p.delay, p.on_timer)
        root_inst.mainloop.assert_called()
        self.assertTrue(p.is_running)

    def test_stop(self, m_world, m_grid, m_tkinter):
        p = presenter.GameOfLifePresenter(5, 6, 123)
        p.start()
        p.stop()

        self.assertFalse(p.is_running)

    def test_on_timer_when_is_running(self, m_world, m_grid, m_tkinter):
        p = presenter.GameOfLifePresenter(5, 6, 123)
        p.start()  # Enable the running state

        p.on_timer()

        world_inst = m_world.return_value
        grid_inst = m_grid.return_value
        root_inst = m_tkinter.Tk.return_value

        world_inst.advance.assert_called()
        grid_inst.set_alives.assert_called_with(world_inst.alives)
        root_inst.after.assert_called_with(p.delay, p.on_timer)

    def test_on_timer_when_not_is_running(self, m_world, m_grid, m_tkinter):
        p = presenter.GameOfLifePresenter(5, 6, 123)

        p.on_timer()

        world_inst = m_world.return_value
        grid_inst = m_grid.return_value
        root_inst = m_tkinter.Tk.return_value

        world_inst.advance.assert_not_called()
        grid_inst.set_alives.assert_not_called()
        root_inst.after.assert_not_called()

    def test_on_cell_click(self, m_world, m_grid, m_tkinter):
        p = presenter.GameOfLifePresenter(5, 6, 123)
        fake_event = mock.Mock()
        fake_event.x = 2
        fake_event.y = 3

        p.on_cell_click(fake_event)

        world_inst = m_world.return_value
        grid_inst = m_grid.return_value

        world_inst.toggle_aliveness.assert_called_with(fake_event.x, fake_event.y)
        grid_inst.set_alives.assert_called_with(world_inst.alives)
