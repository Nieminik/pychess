"""Tests for Bishop class."""

import pytest

from pychess.grid import Grid
from pychess.piece.position import Position, MAX_POS
import pychess.piece.pieces as pieces

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
    bishop = pieces.Bishop(Position(1, 1))
    grid.add_piece(bishop)
    return bishop


@pytest.mark.parametrize("coords", COORDS_GROUP)
def test_bishop_ranges(coords, bishop):  # noqa: D103
    bishop._pos = Position(*coords)

    assert sorted(bishop.move_range) == sorted(bishop.attack_range)
    assert sorted(diagonal(bishop)) == sorted(bishop.move_range)


def test_bishop_incorrect_move(bishop):  # noqa: D103
    assert not bishop.move(bishop.position)
    assert not bishop.move(
        Position(bishop.position.row + 1, bishop.position.col))
    assert not bishop.move(
        Position(bishop.position.row, bishop.position.col + 1))

    assert not bishop.move(Position(MAX_POS, bishop.position.col))
    assert not bishop.move(Position(-1, bishop.position.col))
    assert not bishop.move(Position(bishop.position.row, MAX_POS))
    assert not bishop.move(Position(bishop.position.row, -1))
