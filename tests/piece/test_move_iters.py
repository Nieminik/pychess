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
    piece = Piece((4, 4))
    grid.add_piece(piece)
    return piece


@pytest.fixture
def collision_setup(piece):  # noqa: D103
    grid = piece.grid
    p2 = Piece(piece.position + Position(0, 1),
               piece.color)
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
    p_rank, p_file = piece.position
    for r, f in func(piece):
        p_rank, p_file = transformation(p_rank, p_file)
        assert r == p_rank
        assert f == p_file


@pytest.mark.parametrize("pos", start_positions)
def test_up(piece, pos):  # noqa: D103
    _basic_iters_test_helper(piece, pos, up, lambda r, f: (r + 1, f))


@pytest.mark.parametrize("pos", start_positions)
def test_down(piece, pos):  # noqa: D103
    _basic_iters_test_helper(piece, pos, down, lambda r, f: (r - 1, f))


@pytest.mark.parametrize("pos", start_positions)
def test_left(piece, pos):  # noqa: D103
    _basic_iters_test_helper(piece, pos, left, lambda r, f: (r, f - 1))


@pytest.mark.parametrize("pos", start_positions)
def test_right(piece, pos):  # noqa: D103
    _basic_iters_test_helper(piece, pos, right, lambda r, f: (r, f + 1))


def test_horizontal_center(piece):  # noqa: D103
    start_pos = piece.position
    hor = horizontal(piece)
    p1 = Position(*next(hor))
    assert p1.rank == start_pos.rank

    p2 = Position(*next(hor))
    assert p2.rank == start_pos.rank
    expected = [start_pos.file - 1, start_pos.file + 1]
    assert sorted((p1.file, p2.file)) == expected


@pytest.mark.parametrize("p_file", (MIN_POS, MAX_POS - 1))
def test_horizontal_edge(p_file, piece):  # noqa: D103
    piece._pos = Position(piece.position.rank, p_file)
    start_pos = piece.position
    hor = horizontal(piece)
    p1 = Position(*next(hor))
    diff = 1 if p_file == MIN_POS else -1

    assert p1.file == start_pos.file + diff
    assert p1.rank == start_pos.rank

    p2 = Position(*next(hor))
    assert p2.file == start_pos.file + diff * 2
    assert p2.rank == start_pos.rank


def test_vertical_center(piece):  # noqa: D103
    start_pos = piece.position
    ver = vertical(piece)
    p1 = Position(*next(ver))
    assert p1.file == start_pos.file

    p2 = Position(*next(ver))
    assert p2.file == start_pos.file
    expected = [start_pos.rank - 1, start_pos.rank + 1]
    assert sorted((p1.rank, p2.rank)) == expected


@pytest.mark.parametrize("p_rank", (MIN_POS, MAX_POS - 1))
def test_vertical_edge(p_rank, piece):  # noqa: D103
    piece._pos = Position(p_rank, piece.position.file)
    start_pos = piece.position
    ver = vertical(piece)
    p1 = Position(*next(ver))
    diff = 1 if p_rank == MIN_POS else -1

    assert p1.file == start_pos.file
    assert p1.rank == start_pos.rank + diff

    p2 = Position(*next(ver))
    assert p2.file == start_pos.file
    assert p2.rank == start_pos.rank + diff * 2


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
