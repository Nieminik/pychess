"""Provide generic piece functionality."""

from pychess.piece.color import Color
from pychess.piece.position import Position


class Piece(object):
    """Generic piece class."""

    def __init__(self, position, color=Color.White):
        self.position = Position(*position)
        self.color = color
        self.grid = None
        self.move_attacks = True
        self._mv_range = []
        self.previous_positions = []

    def __eq__(self, other):  # noqa: D105
        eq = isinstance(self, type(other))
        eq *= self.position == other.position
        eq *= self.color == other.color
        eq *= self.moves == other.moves
        return eq

    @property
    def moves(self):  # noqa: D102
        return len(self.previous_positions)

    @property
    def move_range(self):  # noqa: D102
        return self._mv_range

    @property
    def attack_range(self):  # noqa: D102
        return self.move_range

    def move(self, position):  # noqa: D102
        new_pos = Position(*position)

        if not new_pos.is_valid():
            return False

        if position == self.position:
            return False

        if new_pos not in self.move_range + self.attack_range:
            return False

        self.previous_positions.append(self.position)
        self.position = position
        return True

    def revert_move(self):
        """Revert one move."""
        try:
            pos = self.previous_positions.pop()
        except IndexError:
            return False

        self.position = pos
        return True

    def __repr__(self):  # noqa: D105
        msg = f"{self.color.name} {self.__class__.__name__} at {self.position}"
        return msg
