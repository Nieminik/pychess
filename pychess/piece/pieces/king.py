"""Provide king piece functionality."""
from itertools import chain

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

        pieces = self.grid.get_enemies(self)
        ranges = list(chain.from_iterable([p.attack_range for p in pieces]))

        rng = list(hor) + list(ver) + list(diag)
        return [x for x in rng if x not in ranges]
