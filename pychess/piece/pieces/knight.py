"""Provide king piece functionality."""

from itertools import product
from pychess.piece.pieces.base import Piece
from pychess.piece.position import Position


class Knight(Piece):
    """Represent a knight object."""

    @property
    def move_range(self):
        """Get a move range for king."""
        row, col = self.position
        diffs = list(product([1, -1], [2, -2]))
        diffs += [tuple(reversed(x)) for x in diffs]
        rng = []

        for d_row, d_col in diffs:
            n_row, n_col = row + d_row, col + d_col
            pos = Position(n_row, n_col)
            other = self.grid[pos]
            other_is_enemy = not other or other.color == self.color.inverted()
            if pos.is_valid() and other_is_enemy:
                rng.append(pos)
            other_piece = self.grid[pos]
            if other_piece and other_piece.color != self.color:
                rng.append(pos)

        return rng
