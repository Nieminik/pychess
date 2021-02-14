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


INVALID_MOVES = [(1, 0), (0, 1), (-1, 0), (0, -1)]


@pytest.fixture
def bishop():  # noqa: D103
    grid = Grid()
    bishop = pieces.Bishop(Position(1, 1))
    grid.add_piece(bishop)
    return bishop


@pytest.mark.parametrize("coords", COORDS_GROUP)
def test_bishop_ranges(coords, bishop):  # noqa: D103
    bishop.position = Position(*coords)

    assert sorted(bishop.move_range) == sorted(bishop.attack_range)
    assert sorted(diagonal(bishop)) == sorted(bishop.move_range)


@pytest.mark.parametrize("wrong_pos_coords", INVALID_MOVES)
def test_bishop_incorrect_move(wrong_pos_coords, bishop):  # noqa: D103
    assert not bishop.move(bishop.position)
    assert not bishop.move(bishop.position + Position(*wrong_pos_coords))

    assert not bishop.move(Position(MAX_POS, bishop.position.file))
    assert not bishop.move(Position(-1, bishop.position.file))
    assert not bishop.move(Position(bishop.position.rank, MAX_POS))
    assert not bishop.move(Position(bishop.position.rank, -1))
