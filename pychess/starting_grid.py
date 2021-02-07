"""Module related to operations on starting chess setup."""

from pychess.piece.position import Position
from pychess.piece.color import Color
from itertools import chain
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


def prepare_pieces(pieces_notations, color):
    """Prepare pieces for color."""
    iters = []
    for piece_cls, notations in pieces_notations.items():
        pieces = list(map(lambda n: piece_cls(
            Position.get_pos(n), color), notations))
        iters.append(pieces)

    return chain.from_iterable(iters)


def add_pieces(grid, pieces):
    """Add each piece to the grid."""
    for piece in pieces:
        grid.add_piece(piece)


def get_starting_grid():
    """Create grid with starting chess position."""
    grid = Grid()

    for color, pieces_notations in STARTING_NOTATIONS.items():
        pieces = prepare_pieces(pieces_notations, color)
        add_pieces(grid, pieces)

    return grid
