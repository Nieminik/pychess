"""A pawn module."""

from .piece import BasePiece
from src.utils.color import Color


class Pawn(BasePiece):
    """Class that implements Pawn piece."""

    @property
    def range(self):  # noqa: D102
        row, col = self.field
        inc = 1 if self.color == Color.WHITE else -1
        n_row = row + inc

        move_range = [(n_row, col)]
        if not self.moves:
            move_range.append((n_row + inc, col))

        for diag_field in ((n_row, col-1), (n_row, col+1)):
            if self.grid(diag_field):
                move_range.append(diag_field)

        return move_range
