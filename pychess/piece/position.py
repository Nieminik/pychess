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

    @staticmethod
    def translate_pos(pos):
        """Translate chess pos notation to coords tuple."""
        return ord(pos[0]) - ord("a"), int(pos[1]) - 1

    @staticmethod
    def get_pos(pos):
        """Get position from chess notation."""
        return Position(*Position.translate_pos(pos))
