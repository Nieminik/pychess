"""Provide pawn piece functionality."""
from pychess.piece.move_iters import up, down
from pychess.piece.pieces.base import Piece
from pychess.piece.position import Position, MAX_POS, MIN_POS
from pychess.piece.color import Color


class Pawn(Piece):
    """Represent a queen object."""

    def __init__(self, position, color, grid):
        super(Pawn, self).__init__(position, color, grid)
        self.move_attacks = False

    @property
    def move_range(self):
        """Get a move range for pawn."""
        rng = []
        fwd_func = up if self.color == Color.White else down
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
