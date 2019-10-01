"""Tests for grid."""

import pytest
from pychess.grid import Grid
from pychess.piece.pieces.base import Piece
from pychess.piece.color import Color


@pytest.fixture
def grid():  # noqa: D103
    return Grid()
    g.add_piece(
    g.add_piece()
    return g

pieces_groups = (
    (Piece((1, 2), color=Color.White), Piece((1, 1), color=Color.Black)),
    (Piece((2, 3), color=Color.White), Piece((4, 4), color=Color.White)),
    (Piece((1, 2), color=Color.Black), Piece((0, 2), color=Color.Black))    
)

@pytest.mark.parametrize("pieces", pieces_groups)
def test_enemies(grid, pieces):  # noqa: D103
    for piece in pieces:
        grid.add_piece(piece)
    pieces = grid.fields.values()
    assert pieces
    
    for piece in pieces:
        assert grid.get_enemies(piece)
