"""Provide bishop piece functionality."""

from pychess.piece.pieces.base import Piece
from pychess.piece.move_iters import horizontal, vertical


class Rook(Piece):
    """Represent a rook object."""

    @property
    def move_range(self):
        """Get a range for rook."""
        rng = list(horizontal(self)) + list(vertical(self))
        return rng + super(Rook, self).move_range
