"""Provide king piece functionality."""

from itertools import product
from pychess.piece.pieces.base import Piece
from pychess.piece.position import Position


class Knight(Piece):
    """Represent a knight object."""

    @property
    def move_range(self):
        """Get a move range for king."""
        diffs = list(product([1, -1], [2, -2]))
        diffs += [tuple(reversed(x)) for x in diffs]
        rng = []

        for d_row, d_col in diffs:
            pos = self.position + Position(d_row, d_col)
            other = self.grid[pos]
            other_is_friend = other and other.color == self.color

            if pos.is_valid() and not other_is_friend:
                rng.append(pos)

        return rng
