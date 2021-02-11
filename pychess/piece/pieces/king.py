"""Provide king piece functionality."""
from pychess.piece.pieces.base import Piece
from pychess.piece.move_iters import horizontal, vertical, diagonal


class King(Piece):
    """Represent a king object."""

    @property
    def move_range(self):
        """Get a move range for king."""
        hor = horizontal(self, 2)
        ver = vertical(self, 2)
        diag = diagonal(self, 4)

        return list(hor) + list(ver) + list(diag)
