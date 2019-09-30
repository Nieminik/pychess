"""Tests for move iters."""

import pytest
import itertools
from pychess.piece.pieces.base import Piece
from pychess.piece.move_iters import forward, back
from pychess.piece.position import Position
from pychess.grid import Grid


@pytest.fixture
def piece():  # noqa: D103
    grid = Grid()
    return Piece((0, 0), grid=grid)


start_positions = (
    Position(1, 0),
    Position(6, 3),
    Position(2, 7),
)

start_positions = list(Position(*p) for p in itertools.product(range(8), repeat=2))

@pytest.mark.parametrize("pos", start_positions)
def test_forward(piece, pos):  # noqa: D103
    piece._pos = pos
    row, col = piece.position
    for r, c in forward(piece):
        assert r == row + 1
        assert c == col
        row = r


@pytest.mark.parametrize("pos", start_positions)
def test_back(piece, pos):  # noqa: D103
    piece._pos = pos
    row, col = piece.position
    for r, c in back(piece):
        assert r == row - 1
        assert c == col
        row = r
