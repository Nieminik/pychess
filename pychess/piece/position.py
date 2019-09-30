"""Module implementing position functionality."""
from collections import namedtuple

MIN_POS = 0
MAX_POS = 8

position_tup = namedtuple("Position", "row, col")


class Position(position_tup):
    """Position class."""

    def is_valid(self):
        """Validate position."""
        return MIN_POS <= self.row < MAX_POS and MIN_POS <= self.col < MAX_POS
