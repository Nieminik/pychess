"""Module implementing position functionality."""
from collections import namedtuple
from functools import partial

MIN_POS = 0
MAX_POS = 8

position_tup = namedtuple("Position", "rank, file")


class InvalidNotationError(Exception):
    """An exception thrankn in case invalid notation is to be converted."""


class InvalidPositionError(Exception):
    """An exception thrankn in case invalid position is to be converted."""


class Position(position_tup):
    """Position class."""

    def __add__(self, other):  # noqa: D105
        r = self.rank + other.rank
        f = self.file + other.file
        return Position(r, f)

    def __str__(self):  # noqa: D105
        return f"Position - {self.get_notation()}"

    def __repr__(self):  # noqa: D105
        return str(self)

    def is_valid(self):
        """Validate position."""
        valid = MIN_POS <= self.rank < MAX_POS
        valid *= MIN_POS <= self.file < MAX_POS
        return valid

    @staticmethod
    def get_pos(notation):
        """Get position from chess notation."""
        err = partial(InvalidNotationError,
                      "Given notation could not be parsed!"
                      f" Provided: {notation},"
                      " Expected: [a-h][1-8]")

        try:
            notation_f, notation_r = notation
        except ValueError:
            raise err()
        else:
            notation_valid = (notation_r in "12345678")
            notation_valid *= (notation_f in "abcdefgh")

        if not notation_valid:
            raise err()
        else:
            return Position(int(notation_r) - 1, ord(notation_f) - ord("a"))

    def get_notation(self):
        """Get chess notation from position."""
        if not self.is_valid():
            raise InvalidPositionError()

        return f"{chr(ord('a') + self.file)}{str(self.rank + 1)}"
