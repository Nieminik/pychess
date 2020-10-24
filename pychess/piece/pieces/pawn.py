"""Provide pawn piece functionality."""
from enum import Enum

from pychess.piece.color import Color
from pychess.piece.move_iters import up, down
from pychess.piece.pieces.base import Piece
from pychess.piece.position import Position


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
            pos = Position(n_row, n_col)
            other = self.grid[pos]
            if pos.is_valid() and other and other.color != self.color:
                rng.append(pos)

            an_passant_pos = Position(row, n_col)
            other = self.grid[an_passant_pos]
            an_passant = (other and other.moves == 1)
            if pos.is_valid() and an_passant and other.color != self.color:
                rng.append(pos)

        return rng

    def move(self, value):
        """Move, check for an passant capture, report it."""
        new_pos = Position(*value)
        other = self.grid[new_pos]
        report = False
        if new_pos in self.attack_range and other is None:
            report = True
            r, c = new_pos
            curr_r, curr_c = self.position
            other = self.grid[Position(curr_r, c)]

        move_succeeded = super().move(value)
        if report and move_succeeded:
            self.grid.report_capture(other)

        return move_succeeded

    @staticmethod
    def get_direction(pawn):
        """Get direction of pawn."""
        return Direction.Up if pawn.color is Color.White else Direction.Down
