from functools import wraps


class OutOfBoundError(Exception):
    """Exception for coordinate values out of size limit."""
    pass


def check_boundary(f):
    @wraps(f)
    def wrapper(self, x, y, *args, **kwargs):
        if x < 0 or x >= self._size[0] or y < 0 or y >= self._size[1]:
            raise OutOfBoundError('{}, {}'.format(x, y))
        else:
            return f(self, x, y, *args, **kwargs)

    return wrapper


class World(object):

    def __init__(self, x, y):
        if x <= 0:
            raise ValueError('x must be larger than 0')
        if y <= 0:
            raise ValueError('y must be larger than 0')

        self._size = (x, y)
        self._alives = set()
        self._corners = ((0, 0), (x-1, 0), (0, y-1), (x-1, y-1))

    @property
    def size(self):
        return self._size

    @property
    def alives(self):
        return tuple(self._alives)

    @check_boundary
    def set_alive(self, x, y):
        self._alives.add((x, y))

    @check_boundary
    def set_dead(self, x, y):
        if self.is_alive(x, y):
            self._alives.remove((x, y))

    @check_boundary
    def is_alive(self, x, y):
        return (x, y) in self._alives

    @check_boundary
    def toggle_aliveness(self, x, y):
        if self.is_alive(x, y):
            self.set_dead(x, y)
        else:
            self.set_alive(x, y)

    def _calc_neighbors(self, x, y):
        all_nbrs = ((x-1, y-1),
                    (x-1, y),
                    (x-1, y+1),
                    (x, y-1),
                    (x, y+1),
                    (x+1, y-1),
                    (x+1, y),
                    (x+1, y+1))
        return tuple(
            (x, y) for x, y in all_nbrs
            if x >= 0 and x < self._size[0] and y >= 0 and y < self._size[1])

    def _calc_aliveness(self, x, y):
        neighbors = self._calc_neighbors(x, y)
        alive_nbrs_count = len(tuple(nbr for nbr in neighbors
                                     if self.is_alive(nbr[0], nbr[1])))

        if self.is_alive(x, y):
            if alive_nbrs_count in (0, 1):
                return False
            elif alive_nbrs_count in (2, 3):
                return True
            elif alive_nbrs_count >= 4:
                return False
        else:
            if alive_nbrs_count == 3:
                return True
            else:
                return False

    def advance(self):
        next_alives = set()
        for x, y in self._alives:
            nbrs = self._calc_neighbors(x, y)
            for nbr in nbrs:
                if self._calc_aliveness(nbr[0], nbr[1]):
                    next_alives.add(nbr)

        self._alives = next_alives


class Pattern(object):

    def __init__(self, name, alives):
        self._name = name
        self._alives = tuple(alives)

    def __repr__(self):
        return '<Pattern "{}">: {}'.format(self._name, repr(self._alives))

    @property
    def alives(self):
        return tuple(self._alives)

    @property
    def name(self):
        return self._name

    def as_screen_coordinate(self, width, height):
        if not self._alives:
            return tuple()

        min_width = 1 + 2 * max(abs(coor[0]) for coor in self._alives)
        min_height = 1 + 2 * max(abs(coor[1]) for coor in self._alives)

        if width < min_width or height < min_height:
            raise ValueError('Size must be larger than width: {}, height: {}.'.format(
                min_width, min_height))

        result = tuple((c[0] + int(width / 2), -c[1] + int(height / 2))
                       for c in self._alives)

        return result


Patterns = [
    Pattern('Clear', []),
    Pattern('Glider', [(1, 0), (0, 1), (-1, -1), (0, -1), (1, -1)]),
    Pattern('Small Exploder', [(0, 0), (1, 0), (-1, 0), (0, 1), (-1, -1), (1, -1), (0, -2)]),
    Pattern('Exploder', [(0, 2), (0, -2), (-2, 2), (-2, 1), (-2, 0), (-2, -1), (-2, -2),
                         (2, 2), (2, 1), (2, 0), (2, -1), (2, -2)])
]
