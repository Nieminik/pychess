"""Provide bishop piece functionality."""

from pychess.piece.pieces.base import Piece
from pychess.piece.move_iters import diagonal


class Bishop(Piece):
    """Represent a bishop object."""

    @property
    def move_range(self):
        """Get a move range for bishop."""
        return list(diagonal(self)) + super(Bishop, self).move_range
