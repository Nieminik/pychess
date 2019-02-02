"""Module implementing base piece functionality."""

from src.utils.color import Color


class Field(tuple):
    """A field class that defines the piece coordinates."""

    def __new__(cls, x, y):  # noqa: D102
        return super(Field, cls).__new__(cls, (x, y))

    def __init__(self, x, y):
        super(Field, self).__init__()
        self.x, self.y = x, y


class BasePiece(object):
    """Class for the piece base implementation."""

    def __init__(self, x, y, color=Color.WHITE, grid=None):
        self._x = x
        self._y = y
        self.color = color
        self.grid = grid

    def __del__(self):  # noqa: D105
        self.grid.erase(self.field)

    @property
    def field(self):  # noqa: D102
        return Field(self.x, self.y)

    @field.setter
    def field(self, value):  # noqa: D102
        self.grid.move(self.field, value)
        self._x, self._y = value

    @property
    def x(self):  # noqa: D102
        return self._x

    @x.setter
    def x(self, value):  # noqa: D102
        self.field = value, self.y

    @property
    def y(self):  # noqa: D102
        return self._y

    @y.setter
    def y(self, value):  # noqa: D102
        self.field = self.x, value
