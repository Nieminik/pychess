"""Provide queen piece functionality."""

from pychess.piece.pieces.bishop import Bishop
from pychess.piece.pieces.rook import Rook


class Queen(Bishop, Rook):
    """Represent a queen object."""

    @property
    def move_range(self):
        """Get a move range for queen."""
        return super(Queen, self).move_range
