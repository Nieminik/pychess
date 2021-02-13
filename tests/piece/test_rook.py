"""Tests for Rook class."""

import pytest

from pychess.grid import Grid
from pychess.piece.position import Position, MAX_POS
from pychess.piece.pieces.rook import Rook

from pychess.piece.move_iters import horizontal, vertical

from itertools import chain

COORDS_GROUP = (
    (1, 2),
    (2, 1),
    (0, 2),
    (7, 7)
)


INVALID_MOVES = [(1, 1), (-1, -1), (1, -1), (-1, 1)]


@pytest.fixture
def rook():  # noqa: D103
    grid = Grid()
    rook = Rook(Position(1, 1))
    grid.add_piece(rook)
    return rook


@pytest.mark.parametrize("coords", COORDS_GROUP)
def test_rook_ranges(coords, rook):  # noqa: D103
    rook.move(coords)
    rook.grid.add_piece(rook)

    assert sorted(rook.move_range) == sorted(rook.attack_range)

    test_range = chain(horizontal(rook), vertical(rook))
    assert sorted(test_range) == sorted(rook.move_range)


@pytest.mark.parametrize("wrong_pos_coords", INVALID_MOVES)
def test_rook_incorrect_move(wrong_pos_coords, rook):  # noqa: D103
    assert not rook.move(rook.position)
    assert not rook.move(rook.position + Position(*wrong_pos_coords))

    assert not rook.move(Position(MAX_POS, rook.position.file))
    assert not rook.move(Position(-1, rook.position.file))
    assert not rook.move(Position(rook.position.rank, MAX_POS))
    assert not rook.move(Position(rook.position.rank, -1))
