"""Tests for move iters."""

import pytest
import itertools
from pychess.piece.pieces.base import Piece
from pychess.piece.move_iters import forward, back, left, right
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

def basic_iters_test_helper(piece, pos, func, transformation):
    piece._pos = pos
    row, col = piece.position
    for r, c in func(piece):
        row, col = transformation(row, col)
        assert r == row
        assert c == col

@pytest.mark.parametrize("pos", start_positions)
def test_forward(piece, pos):  # noqa: D103
    basic_iters_test_helper(piece, pos, forward, lambda r, c: (r + 1, c))


@pytest.mark.parametrize("pos", start_positions)
def test_back(piece, pos):  # noqa: D103
    basic_iters_test_helper(piece, pos, forward, lambda r, c: (r - 1, c))


@pytest.mark.parametrize("pos", start_positions)
def test_left(piece, pos):  # noqa: D103
    basic_iters_test_helper(piece, pos, left, lambda r, c: (r, c - 1))


@pytest.mark.parametrize("pos", start_positions)
def test_right(piece, pos):  # noqa: D103
    basic_iters_test_helper(piece, pos, right, lambda r, c: (r, c + 1))
