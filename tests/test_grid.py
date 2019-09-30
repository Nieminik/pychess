"""Tests for grid."""

import pytest
from pychess.grid import Grid
from pychess.piece.pieces.base import Piece
from pychess.piece.color import Color


@pytest.fixture
def grid():  # noqa: D103
    g = Grid()
    g.add_piece(Piece((1, 1), color=Color.Black))
    g.add_piece(Piece((1, 2), color=Color.White))
    return g


def test_enemies(grid):  # noqa: D103
    for piece in grid.fields.values():
        assert grid.get_enemies(piece)
