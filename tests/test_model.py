import unittest

from game_of_life.model import World
from game_of_life.model import Pattern
from game_of_life.model import OutOfBoundError


class PatternTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        # The "Glider" pattern
        pattern = Pattern('Glider', alives=[(1, 0), (0, 1), (-1, -1), (0, -1), (1, -1)])

        self.assertIsInstance(pattern, Pattern)
        self.assertEqual(pattern.name, 'Glider')

    def test_repr(self):
        pattern = Pattern('FooBar', alives=[(1, 0), (0, 1)])

        r = repr(pattern)

        self.assertEqual(r,
                         '<Pattern "FooBar">: ((1, 0), (0, 1))')

    def test_as_screen_coordinate(self):
        pattern = Pattern('Glider', alives=[(1, 0), (0, 1), (-1, -1), (0, -1), (1, -1)])

        r = pattern.as_screen_coordinate(width=11, height=33)

        # Formula:
        # x' = x + int(width / 2)
        # y' = -y + int(height / 2)
        self.assertEqual(r,
                         ((6, 16),
                          (5, 15),
                          (4, 17),
                          (5, 17),
                          (6, 17)))

    def test_as_screen_coordinate_empty_pattern(self):
        pattern = Pattern('Glider', alives=[])

        r = pattern.as_screen_coordinate(width=11, height=33)

        self.assertEqual(r, tuple())

    def test_as_screen_coordinate_error_size_too_small(self):
        pattern = Pattern('FooBar', alives=[(10, 5), (-8, -10)])

        # Formula:
        # width = 1 + 2 * max(abs(x) for x in all_x)
        # height = 1 + 2 * max(abs(y) for y in all_y)
        with self.assertRaisesRegex(ValueError,
                                    r'Size must be larger than width: 21, height: 21.'):
            pattern.as_screen_coordinate(20, 20)


class WorldTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_x_y(self):
        world = World(x=20, y=30)

        self.assertIsInstance(world, World)
        self.assertEqual(world.size, (20, 30))

    def test_init_x_or_y_error(self):
        with self.assertRaises(ValueError):
            World(x=-10, y=10)
        with self.assertRaises(ValueError):
            World(x=-0, y=10)

        with self.assertRaises(ValueError):
            World(x=10, y=-10)
        with self.assertRaises(ValueError):
            World(x=10, y=0)

        with self.assertRaises(ValueError):
            World(x=-10, y=-10)
        with self.assertRaises(ValueError):
            World(x=0, y=0)

    def test_set_alive(self):
        world = World(20, 30)

        world.set_alive(2, 3)

        self.assertEqual(world.is_alive(2, 3), True)

    def test_set_alive_out_of_bound(self):
        world = World(20, 30)

        with self.assertRaises(OutOfBoundError):
            world.set_alive(20, 30)

    def test_is_alive(self):
        world = World(20, 30)

        world.set_alive(2, 3)

        self.assertEqual(world.is_alive(2, 3), True)

    def test_is_alive_out_of_bound(self):
        world = World(20, 30)

        with self.assertRaises(OutOfBoundError):
            world.is_alive(20, 30)

    def test_set_dead(self):
        world = World(20, 30)

        world.set_alive(2, 3)
        world.set_dead(2, 3)

        self.assertEqual(world.is_alive(2, 3), False)

    def test_set_dead_out_of_bound(self):
        world = World(20, 30)

        with self.assertRaises(OutOfBoundError):
            world.set_dead(20, 30)

    def test_set_dead_for_not_alives(self):
        world = World(20, 30)
        world.set_dead(3, 4)

        self.assertEqual(world.is_alive(3, 4), False)

    def test_toggle_aliveness_from_dead(self):
        world = World(20, 30)
        world.set_dead(2, 3)

        world.toggle_aliveness(2, 3)

        self.assertEqual(world.is_alive(2, 3), True)

    def test_toggle_aliveness_from_alive(self):
        world = World(20, 30)
        world.set_alive(2, 3)

        world.toggle_aliveness(2, 3)

        self.assertEqual(world.is_alive(2, 3), False)

    def test_toggle_aliveness_out_of_bound(self):
        world = World(20, 30)

        with self.assertRaises(OutOfBoundError):
            world.toggle_aliveness(20, 30)

    def test_get_alives(self):
        world = World(20, 30)

        world.set_alive(2, 3)
        world.set_alive(10, 20)

        self.assertEqual(world.alives,
                         ((2, 3), (10, 20)))

    def test_calc_neighbors(self):
        world = World(20, 30)

        neighbors = world._calc_neighbors(3, 4)

        self.assertIsInstance(neighbors, tuple)
        self.assertEqual(len(neighbors), 8)
        self.assertCountEqual(neighbors,
                              ((2, 3),
                               (2, 4),
                               (2, 5),
                               (3, 3),
                               (3, 5),
                               (4, 3),
                               (4, 4),
                               (4, 5)))

    def test_calc_neighbors_at_bottom_left_corners(self):
        world = World(20, 30)

        neighbors = world._calc_neighbors(0, 0)

        self.assertIsInstance(neighbors, tuple)
        self.assertEqual(len(neighbors), 3)
        self.assertCountEqual(neighbors,
                              ((0, 1),
                               (1, 0),
                               (1, 1)))

    def test_calc_neighbors_at_bottom_right_corners(self):
        world = World(20, 30)

        neighbors = world._calc_neighbors(19, 0)

        self.assertIsInstance(neighbors, tuple)
        self.assertEqual(len(neighbors), 3)
        self.assertCountEqual(neighbors,
                              ((18, 0),
                               (18, 1),
                               (19, 1)))

    def test_calc_neighbors_at_upper_left_corners(self):
        world = World(20, 30)

        neighbors = world._calc_neighbors(0, 29)

        self.assertIsInstance(neighbors, tuple)
        self.assertEqual(len(neighbors), 3)
        self.assertCountEqual(neighbors,
                              ((0, 28),
                               (1, 28),
                               (1, 29)))

    def test_calc_neighbors_at_upper_right_corners(self):
        world = World(20, 30)

        neighbors = world._calc_neighbors(19, 29)

        self.assertIsInstance(neighbors, tuple)
        self.assertCountEqual(neighbors,
                              ((18, 28),
                               (18, 29),
                               (19, 28)))

    def test_calc_neighbors_on_left_side(self):
        world = World(20, 30)

        neighbors = world._calc_neighbors(0, 5)

        self.assertIsInstance(neighbors, tuple)
        self.assertCountEqual(neighbors,
                              ((0, 6),
                               (1, 6),
                               (1, 5),
                               (1, 4),
                               (0, 4)))

    def test_calc_neighbors_on_right_side(self):
        world = World(20, 30)

        neighbors = world._calc_neighbors(19, 5)

        self.assertIsInstance(neighbors, tuple)
        self.assertCountEqual(neighbors,
                              ((19, 6),
                               (18, 6),
                               (18, 5),
                               (18, 4),
                               (19, 4)))

    def test_calc_neighbors_on_upper_side(self):
        world = World(20, 30)

        neighbors = world._calc_neighbors(5, 29)

        self.assertIsInstance(neighbors, tuple)
        self.assertCountEqual(neighbors,
                              ((4, 29),
                               (4, 28),
                               (5, 28),
                               (6, 28),
                               (6, 29)))

    def test_calc_neighbors_on_bottom_side(self):
        world = World(20, 30)

        neighbors = world._calc_neighbors(5, 0)

        self.assertIsInstance(neighbors, tuple)
        self.assertEqual(len(neighbors), 5)
        self.assertCountEqual(neighbors,
                              ((4, 0),
                               (4, 1),
                               (5, 1),
                               (6, 1),
                               (6, 0)))

    def test_calc_aliveness_died_by_no_neighbor(self):
        world = World(20, 30)

        world.set_alive(5, 5)

        self.assertEqual(world._calc_aliveness(5, 5), False)
        self.assertEqual(world._calc_aliveness(5, 6), False)

    def test_calc_aliveness_died_by_one_neighbor(self):
        world = World(20, 30)

        world.set_alive(5, 5)
        world.set_alive(5, 6)

        self.assertEqual(world._calc_aliveness(5, 5), False)
        self.assertEqual(world._calc_aliveness(5, 6), False)

    def test_calc_aliveness_died_by_four_neighbors(self):
        world = World(20, 30)

        world.set_alive(5, 5)
        world.set_alive(5, 6)
        world.set_alive(5, 4)
        world.set_alive(6, 5)
        world.set_alive(6, 4)

        self.assertEqual(world._calc_aliveness(5, 5), False)
        self.assertEqual(world._calc_aliveness(6, 5), False)

    def test_calc_aliveness_died_by_five_neighbors(self):
        world = World(20, 30)

        world.set_alive(5, 5)
        world.set_alive(5, 6)
        world.set_alive(5, 4)
        world.set_alive(6, 5)
        world.set_alive(6, 4)
        world.set_alive(6, 6)

        self.assertEqual(world._calc_aliveness(5, 5), False)
        self.assertEqual(world._calc_aliveness(6, 5), False)

    def test_calc_aliveness_survive_by_two_neighbors(self):
        world = World(20, 30)

        world.set_alive(5, 5)
        world.set_alive(6, 6)
        world.set_alive(4, 4)

        self.assertEqual(world._calc_aliveness(5, 5), True)

    def test_calc_aliveness_survive_by_three_neighbors(self):
        world = World(20, 30)

        world.set_alive(5, 5)
        world.set_alive(5, 6)
        world.set_alive(6, 6)
        world.set_alive(6, 5)

        self.assertEqual(world._calc_aliveness(5, 5), True)
        self.assertEqual(world._calc_aliveness(5, 6), True)
        self.assertEqual(world._calc_aliveness(6, 6), True)
        self.assertEqual(world._calc_aliveness(6, 5), True)

    def test_calc_aliveness_populated(self):
        world = World(20, 30)

        world.set_alive(4, 6)
        world.set_alive(4, 4)
        world.set_alive(6, 5)

        self.assertEqual(world._calc_aliveness(5, 5), True)

    def test_calc_aliveness_not_populated_with_two_neighbors(self):
        world = World(20, 30)

        world.set_alive(6, 5)
        world.set_alive(4, 5)

        self.assertEqual(world._calc_aliveness(5, 5), False)

    def test_calc_alivness_not_populated_with_four_neighbors(self):
        world = World(20, 30)

        world.set_alive(6, 5)
        world.set_alive(4, 5)
        world.set_alive(5, 6)
        world.set_alive(5, 4)

        self.assertEqual(world._calc_aliveness(5, 5), False)

    def test_calc_aliveness_bottom_left_corner_alive(self):
        world = World(10, 10)

        world.set_alive(0, 0)
        world.set_alive(0, 1)
        world.set_alive(1, 0)

        self.assertEqual(world._calc_aliveness(0, 0), True)
        self.assertEqual(world._calc_aliveness(0, 1), True)
        self.assertEqual(world._calc_aliveness(1, 0), True)
        self.assertEqual(world._calc_aliveness(1, 1), True)

    def test_calc_aliveness_bottom_right_corner_alive(self):
        world = World(10, 10)

        world.set_alive(9, 0)
        world.set_alive(8, 0)
        world.set_alive(9, 1)

        self.assertEqual(world._calc_aliveness(9, 0), True)
        self.assertEqual(world._calc_aliveness(9, 1), True)
        self.assertEqual(world._calc_aliveness(8, 0), True)
        self.assertEqual(world._calc_aliveness(8, 1), True)

    def test_calc_aliveness_upper_left_corner_alive(self):
        world = World(10, 10)

        world.set_alive(0, 9)
        world.set_alive(0, 8)
        world.set_alive(1, 9)

        self.assertEqual(world._calc_aliveness(0, 9), True)
        self.assertEqual(world._calc_aliveness(0, 8), True)
        self.assertEqual(world._calc_aliveness(1, 9), True)
        self.assertEqual(world._calc_aliveness(1, 8), True)

    def test_calc_aliveness_upper_right_corner_alive(self):
        world = World(10, 10)

        world.set_alive(9, 9)
        world.set_alive(8, 9)
        world.set_alive(9, 8)

        self.assertEqual(world._calc_aliveness(9, 9), True)
        self.assertEqual(world._calc_aliveness(8, 9), True)
        self.assertEqual(world._calc_aliveness(9, 8), True)
        self.assertEqual(world._calc_aliveness(8, 8), True)

    def test_advance(self):
        world = World(10, 10)
        world.set_alive(9, 9)
        world.set_alive(8, 9)
        world.set_alive(9, 8)
        self.assertCountEqual(world.alives,
                              ((9, 9),
                               (8, 9),
                               (9, 8)))

        world.advance()

        self.assertCountEqual(world.alives,
                              ((9, 9),
                               (8, 9),
                               (9, 8),
                               (8, 8)))
