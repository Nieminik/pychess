"""Tests for move iters."""

import pytest

from pychess.grid import Grid
from pychess.piece.move_iters import up, down, left, right, horizontal, \
    vertical
from pychess.piece.pieces.base import Piece
from pychess.piece.position import Position, MAX_POS, MIN_POS


@pytest.fixture
def piece():  # noqa: D103
    grid = Grid()
    return Piece((4, 4), grid=grid)


@pytest.fixture
def collision_setup(piece):  # noqa: D103
    grid = piece.grid
    p2 = Piece(Position(piece.position.row, piece.position.col + 1),
               piece.color, grid)
    grid.add_piece(piece)
    grid.add_piece(p2)
    r = right(piece)
    return piece, p2, r


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


def test_vertical_center(piece):  # noqa: D103
    row, col = piece.position
    ver = vertical(piece)
    n1_row, n_col = next(ver)
    assert n_col == col

    n2_row, n_col = next(ver)
    assert n_col == col
    assert sorted((n1_row, n2_row)) == [row - 1, row + 1]


@pytest.mark.parametrize("row", (MIN_POS, MAX_POS - 1))
def test_vertical_edge(row, piece):  # noqa: D103
    piece._pos = Position(row, piece.position.col)
    row, col = piece.position
    ver = vertical(piece)
    n_row, n_col = next(ver)
    diff = 1 if row == MIN_POS else -1

    assert n_col == col
    assert n_row == row + diff

    n_row, n_col = next(ver)
    assert n_col == col
    assert n_row == row + diff * 2


def _hor_ver_max_iters_helper(piece, it_f):  # noqa: D103
    iters = [it_f(piece, i) for i in range(3)]
    for i, it in enumerate(iters):
        for _ in range(i):
            next(it)

        with pytest.raises(StopIteration):
            next(it)


def test_horizontal_max_iters(piece):  # noqa: D103
    _hor_ver_max_iters_helper(piece, horizontal)


def test_vertical_max_iters(piece):  # noqa: D103
    _hor_ver_max_iters_helper(piece, vertical)


def test_iter_collision_ally(collision_setup):  # noqa: D103
    p1, p2, r = collision_setup
    with pytest.raises(StopIteration):
        next(r)


def test_iter_collision_enemy(collision_setup):  # noqa: D103
    p1, p2, r = collision_setup
    p2.color = p2.color.inverted()
    next(r)
    with pytest.raises(StopIteration):
        next(r)
