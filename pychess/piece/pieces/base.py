"""Provide generic piece functionality."""

from pychess.piece.color import Color
from pychess.piece.position import Position


class Piece(object):
    """Generic piece class."""

    def __init__(self, position, color=Color.White):
        self._pos = Position(*position)
        self.color = color
        self.grid = None
        self.moves = 0
        self.move_attacks = True
        self._mv_range = []

    def __eq__(self, other):  # noqa: D105
        eq = isinstance(self, type(other))
        eq *= self._pos == other._pos
        eq *= self.color == other.color
        eq *= self.grid == other.grid
        eq *= self.moves == other.moves
        return eq

    @property
    def move_range(self):  # noqa: D102
        return self._mv_range

    @property
    def attack_range(self):  # noqa: D102
        return self.move_range

    @property
    def position(self):  # noqa: D102
        return self._pos

    def move(self, position):  # noqa: D102
        new_pos = Position(*position)

        if not new_pos.is_valid():
            return False

        if new_pos not in self.move_range + self.attack_range:
            return False

        old_pos = self.position
        if position == self._pos:
            return False

        if self.grid and not self.grid.can_move(old_pos, new_pos):
            return False

        self.moves += 1
        self._pos = position
        return True

    def __repr__(self):  # noqa: D105
        msg = f"{self.color.name} {self.__class__.__name__} at {self.position}"
        return msg
