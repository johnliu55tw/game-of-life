import unittest

from game_of_life import World
from game_of_life.world import OutOfBoundError


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

    def test_alived_then_died_by_solitude(self):
        world = World(10, 10)
        world.set_alive(5, 5)

        world.advance()

        self.assertEqual(world.is_alive(5, 5), False)
        self.assertEqual(world.alives, tuple())

    def test_alived_then_died_by_one_neighbor(self):
        world = World(10, 10)
        world.set_alive(5, 5)
        world.set_alive(5, 6)

        world.advance()

        self.assertEqual(world.is_alive(5, 5), False)
        self.assertEqual(world.is_alive(5, 6), False)
        self.assertEqual(len(world.alives), 0)

    def test_alived_then_died_by_overpopulation(self):
        world = World(10, 10)
        world.set_alive(5, 5)
        world.set_alive(5, 6)
        world.set_alive(5, 4)
        world.set_alive(6, 5)
        world.set_alive(6, 4)

        world.advance()

        self.assertEqual(world.is_alive(5, 5), False)
        self.assertEqual(world.is_alive(6, 5), False)

    def test_alived_then_survived(self):
        world = World(10, 10)
        world.set_alive(5, 5)
        world.set_alive(6, 5)
        world.set_alive(5, 6)

        world.advance()

        self.assertEqual(world.is_alive(5, 5), True)
        self.assertEqual(world.is_alive(6, 5), True)
        self.assertEqual(world.is_alive(5, 6), True)

    def test_died_become_alive(self):
        world = World(10, 10)
        world.set_alive(5, 5)
        world.set_alive(6, 5)
        world.set_alive(5, 6)

        world.advance()

        self.assertEqual(world.is_alive(6, 6), True)

    def test_alive_bottom_left_corner(self):
        world = World(10, 10)
        world.set_alive(0, 0)
        world.set_alive(0, 1)
        world.set_alive(1, 0)

        world.advance()

        self.assertEqual(world.is_alive(0, 0), True)
        self.assertEqual(world.is_alive(0, 1), True)
        self.assertEqual(world.is_alive(1, 0), True)
        self.assertEqual(world.is_alive(1, 1), True)
