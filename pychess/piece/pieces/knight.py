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

        # TODO: Change this so _pos_iter is used.
        # This is lacking other pieces recognition.
        for d_row, d_col in diffs:
            n_row, n_col = row + d_row, col + d_col
            pos = Position(n_row, n_col)
            if pos.is_valid():
                rng.append(pos)

        return rng
