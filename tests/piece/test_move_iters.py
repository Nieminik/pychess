"""Tests for move iters."""

import pytest

from pychess.grid import Grid
from pychess.piece.move_iters import up, down, left, right, horizontal
from pychess.piece.pieces.base import Piece
from pychess.piece.position import Position, MAX_POS, MIN_POS


@pytest.fixture
def piece():  # noqa: D103
    grid = Grid()
    return Piece((4, 4), grid=grid)


start_positions = (
    Position(1, 0),
    Position(6, 3),
    Position(2, 7),
)


def _basic_iters_test_helper(piece, pos, func, transformation):
    piece._pos = pos
    row, col = piece.position
    for r, c in func(piece):
        row, col = transformation(row, col)
        assert r == row
        assert c == col


@pytest.mark.parametrize("pos", start_positions)
def test_up(piece, pos):  # noqa: D103
    _basic_iters_test_helper(piece, pos, up, lambda r, c: (r + 1, c))


@pytest.mark.parametrize("pos", start_positions)
def test_down(piece, pos):  # noqa: D103
    _basic_iters_test_helper(piece, pos, down, lambda r, c: (r - 1, c))


@pytest.mark.parametrize("pos", start_positions)
def test_left(piece, pos):  # noqa: D103
    _basic_iters_test_helper(piece, pos, left, lambda r, c: (r, c - 1))


@pytest.mark.parametrize("pos", start_positions)
def test_right(piece, pos):  # noqa: D103
    _basic_iters_test_helper(piece, pos, right, lambda r, c: (r, c + 1))


def test_horizontal_center(piece):  # noqa: D103
    row, col = piece.position
    hor = horizontal(piece)
    n_row, n1_col = next(hor)
    assert n_row == row

    n_row, n2_col = next(hor)
    assert n_row == row
    assert sorted((n1_col, n2_col)) == [col - 1, col + 1]


@pytest.mark.parametrize("col", (MIN_POS, MAX_POS - 1))
def test_horizontal_edge(col, piece):  # noqa: D103
    piece._pos = Position(piece.position.row, col)
    row, col = piece.position
    hor = horizontal(piece)
    n_row, n_col = next(hor)
    diff = 1 if col == MIN_POS else -1

    assert n_col == col + diff
    assert n_row == row

    n_row, n_col = next(hor)
    assert n_col == col + diff * 2
    assert n_row == row


def test_horizontal_max_iters(piece):  # noqa: D103
    hors = [horizontal(piece, i) for i in range(3)]
    for i, hor in enumerate(hors):
        for _ in range(i):
            next(hor)

        with pytest.raises(StopIteration):
            next(hor)
