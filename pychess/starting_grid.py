"""Module related to operations on starting chess setup."""

from pychess.piece.position import Position
from pychess.piece.color import Color
import pychess.piece.pieces as pieces

from pychess.grid import Grid


STARTING_NOTATIONS = {
    Color.White: {
        pieces.Pawn: tuple((f"{c}2" for c in "abcdefgh")),
        pieces.Rook: ("a1", "h1"),
        pieces.Knight: ("b1", "g1"),
        pieces.Bishop: ("c1", "f1"),
        pieces.Queen: ("d1",),
        pieces.King: ("e1",)
    },

    Color.Black: {
        pieces.Pawn: tuple((f"{c}7" for c in "abcdefgh")),
        pieces.Rook: ("a8", "h8"),
        pieces.Knight: ("b8", "g8"),
        pieces.Bishop: ("c8", "f8"),
        pieces.Queen: ("d8",),
        pieces.King: ("e8",)
    }
}


def get_starting_grid():
    """Create grid with starting chess position."""
    grid = Grid()

    for color, piece_notations in STARTING_NOTATIONS.items():
        for piece_cls, notations in piece_notations.items():
            for notation_pos in notations:
                piece = piece_cls(Position.get_pos(notation_pos), color)
                grid.add_piece(piece)

    return grid
