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
        self._alives.remove((x, y))

    @check_boundary
    def is_alive(self, x, y):
        return (x, y) in self._alives

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