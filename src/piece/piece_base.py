"""Module implementing base piece functionality."""
import itertools
from src.utils.color import Color
from collections import namedtuple

Field = namedtuple("Field", ("row", "col"))


class BasePiece(object):
    """Class for the piece base implementation."""

    def __init__(self, row, col, color=Color.WHITE, grid=None):
        self._row = row
        self._col = col
        self.color = color
        self._grid = grid
        self.moves = 0

    @property
    def field(self):  # noqa: D102
        return Field(self.row, self.col)

    @field.setter
    def field(self, value):  # noqa: D102
        self.moves += 1
        self._row, self._col = value

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

    @property
    def range(self):  # noqa: D102
        return itertools.product(range(8), repeat=2)
