"""Provide pawn piece functionality."""
from pychess.piece.move_iters import up, down
from pychess.piece.pieces.base import Piece
from pychess.piece.position import Position, MAX_POS, MIN_POS
from pychess.piece.color import Color
from enum import Enum


class Direction(Enum):
    """Pawn move direction enum."""

    Down = -1
    Up = 1


class Pawn(Piece):
    """Represent a queen object."""

    def __init__(self, position, color=Color.White, grid=None):
        super(Pawn, self).__init__(position, color, grid)
        self.move_attacks = False

    @property
    def move_range(self):
        """Get a move range for pawn."""
        rng = []
        fwd_func = {Direction.Up: up,
                    Direction.Down: down}[self.get_direction(self)]
        fwd = fwd_func(self)
        for pos, move_cond in zip(fwd, (True, not self.moves)):
            if pos and move_cond:
                rng.append(Position(*pos))

        return rng

    @property
    def attack_range(self):
        """Get an attack range for pawn."""
        row, col = self.position
        n_row = row + self.get_direction(self).value
        rng = []

        for n_col in (col + 1, col - 1):
            if n_col in range(MIN_POS, MAX_POS):
                rng.append(Position(n_row, n_col))

        return rng

    @staticmethod
    def get_direction(pawn):
        """Get direction of pawn."""
        return Direction.Up if pawn.color is Color.White else Direction.Down
