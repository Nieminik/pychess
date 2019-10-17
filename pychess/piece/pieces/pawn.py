"""Provide pawn piece functionality."""

from pychess.piece.pieces.base import Piece
from pychess.piece.position import Position, MAX_POS, MIN_POS
from pychess.piece.color import Color
import pychess.piece.move_iters as m_iters


class Pawn(Piece):
    """Represent a queen object."""

    @property
    def move_range(self):
        """Get a move range for pawn."""
        rng = []
        fwd_func = m_iters.up if self.color == Color.White else m_itsrs.down
        fwd = fwd_func(self)
        for pos, move_cond in zip(fwd, (True, not self.moves)):
            if pos and move_cond:
                rng.append(Position(*pos))

        return rng

    @property
    def attack_range(self):
        """Get an attack range for pawn."""
        row, col = self.position
        n_row = row + (1 if self.color is Color.White else -1)
        rng = []

        for n_col in (col + 1, col - 1):
            if n_col in range(MIN_POS, MAX_POS):
                rng.append(Position(n_row, n_col))

        return rng
