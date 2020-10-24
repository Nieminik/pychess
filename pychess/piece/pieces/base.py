"""Provide generic piece functionality."""

from pychess.piece.color import Color
from pychess.piece.position import Position


class Piece(object):
    """Generic piece class."""

    def __init__(self, position, color=Color.White, grid=None):
        self._pos = Position(*position)
        self.color = color
        self.grid = grid
        self.moves = 0
        self.move_attacks = True
        self._mv_range = []

    @property
    def move_range(self):  # noqa: D102
        return self._mv_range

    @property
    def attack_range(self):  # noqa: D102
        return self.move_range

    @property
    def position(self):  # noqa: D102
        return self._pos

    def move(self, value):  # noqa: D102
        new_pos = Position(*value)
        if new_pos != self._pos and new_pos in self.move_range:
            self.moves += 1
            self._pos = new_pos
            return True

        return False

    def __repr__(self):  # noqa: D105
        msg = f"{self.color.name} {self.__class__.__name__} at {self.position}"
        return msg
