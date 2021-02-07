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

    def move_raw(self, position):
        if position == self._pos:
            return False

        self.moves += 1
        self._pos = position
        return True

    def move(self, position):  # noqa: D102
        new_pos = Position(*position)
        if new_pos in self.move_range:
            return self.move_raw(new_pos)

        return False

    def __repr__(self):  # noqa: D105
        msg = f"{self.color.name} {self.__class__.__name__} at {self.position}"
        return msg
