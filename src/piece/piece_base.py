"""Module implementing base piece functionality."""
from src.chess_grid import GridMoveError
from src.utils.color import Color


class Field(tuple):
    """A field class that defines the piece coordinates."""

    def __new__(cls, row, col):  # noqa: D102
        return super(Field, cls).__new__(cls, (row, col))

    def __init__(self, row, col):
        super(Field, self).__init__()
        self.row, self.col = row, col


class BasePiece(object):
    """Class for the piece base implementation."""

    def __init__(self, row, col, color=Color.WHITE, grid=None):
        self._row = row
        self._col = col
        self.color = color
        self.grid = grid

    def __del__(self):  # noqa: D105
        self.grid.erase(self.field)

    @property
    def field(self):  # noqa: D102
        return Field(self.row, self.col)

    @field.setter
    def field(self, value):  # noqa: D102
        try:
            self.grid.move(self.field, value)
            self._row, self._col = value
        except GridMoveError:
            pass

    @property
    def row(self):  # noqa: D102
        return self._row

    @row.setter
    def row(self, value):  # noqa: D102
        self.field = value, self.col

    @property
    def col(self):  # noqa: D102
        return self._col

    @col.setter
    def col(self, value):  # noqa: D102
        self.field = self.row, value
