"""Tests for Bishop class."""

import pytest

from pychess.grid import Grid
from pychess.piece.position import Position
from pychess.piece.pieces.bishop import Bishop

from pychess.piece.move_iters import diagonal

COORDS_GROUP = (
    (1, 2),
    (2, 1),
    (0, 2),
    (7, 7)
)


@pytest.fixture
def bishop():  # noqa: D103
    grid = Grid()
    return Bishop(Position(1, 1), grid=grid)


@pytest.mark.parametrize("coords", COORDS_GROUP)
def test_bishop_ranges(coords, bishop):  # noqa: D103
    bishop.move(coords)
    bishop.grid.add_piece(bishop)

    assert sorted(bishop.move_range) == sorted(bishop.attack_range)
    assert sorted(diagonal(bishop)) == sorted(bishop.move_range)
