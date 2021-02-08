"""Tests for Rook class."""

import pytest

from pychess.grid import Grid
from pychess.piece.position import Position
from pychess.piece.pieces.rook import Rook

from pychess.piece.move_iters import horizontal, vertical

from itertools import chain

COORDS_GROUP = (
    (1, 2),
    (2, 1),
    (0, 2),
    (7, 7)
)


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
