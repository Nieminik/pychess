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
    """Represent a pawn object."""

    def __init__(self, position, color=Color.White):
        super().__init__(position, color)
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
            if pos.is_valid() and (not other or other.color != self.color):
                rng.append(pos)

        return rng

    def move(self, value):
        """Move, check for an passant capture, report it."""
        new_pos = Position(*value)

        other = self.grid[new_pos]
        an_passant = False
        if new_pos in self.move_range:
            move_possible = True
        elif new_pos in self.attack_range and other:
            move_possible = other.color is not self.color
        else:
            dir_val = self.get_direction(self).value
            an_passant_pos = Position(new_pos.row - dir_val, new_pos.col)
            an_passant_victim = self.grid[an_passant_pos]
            move_possible = Pawn._can_be_captured_an_passant(
                an_passant_victim, self)
            an_passant = move_possible and an_passant_victim

        move_succeeded = super().move(new_pos) if move_possible else False

        if move_succeeded and an_passant:
            self.grid.report_capture(an_passant)

        return move_succeeded

    @staticmethod
    def get_direction(pawn):
        """Get direction of pawn."""
        return Direction.Up if pawn.color is Color.White else Direction.Down

    @staticmethod
    def _can_be_captured_an_passant(piece, attacker):
        if piece is None:
            return False

        condition = piece.color != attacker.color
        condition *= piece.moves == 1
        condition *= isinstance(piece, Pawn)

        return condition
