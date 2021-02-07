"""Module implementing position functionality."""
from collections import namedtuple

MIN_POS = 0
MAX_POS = 8

position_tup = namedtuple("Position", "row, col")


class InvalidNotationError(Exception):
    """An exception thrown in case invalid notation is to be converted."""


class InvalidPositionError(Exception):
    """An exception thrown in case invalid position is to be converted."""


class Position(position_tup):
    """Position class."""

    def is_valid(self):
        """Validate position."""
        return MIN_POS <= self.row < MAX_POS and MIN_POS <= self.col < MAX_POS

    @staticmethod
    def get_pos(notation):
        """Get position from chess notation."""
        try:
            notation_c, notation_r = notation
        except ValueError:
            input_valid = False
        else:
            input_valid = notation_r in "12345678"
            input_valid *= notation_c in "abcdefgh"

        if not input_valid:
            raise InvalidNotationError()

        return Position(int(notation_r) - 1, ord(notation_c) - ord("a"))

    def get_notation(self):
        """Get chess notation from position."""
        if not self.is_valid():
            raise InvalidPositionError()

        return f"{chr(ord('a') + self.col)}{str(self.row + 1)}"
