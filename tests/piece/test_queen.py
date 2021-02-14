"""Tests for Queen class."""

import pytest

from pychess.grid import Grid
from pychess.piece.position import Position, MAX_POS
import pychess.piece.pieces as pieces

from pychess.piece.move_iters import diagonal, horizontal, vertical

from itertools import chain

COORDS_GROUP = (
    (1, 2),
    (2, 1),
    (0, 2),
    (7, 7)
)


INVALID_MOVES = [(1, 2), (1, -2), (-1, 2), (-1, -2)]
INVALID_MOVES += list(map(reversed, INVALID_MOVES))


@pytest.fixture
def queen():  # noqa: D103
    grid = Grid()
    queen = pieces.Queen(Position(1, 1))
    grid.add_piece(queen)
    return queen


@pytest.mark.parametrize("coords", COORDS_GROUP)
def test_queen_ranges(coords, queen):  # noqa: D103
    queen.position = Position(*coords)

    exp_ranges = chain(diagonal(queen), horizontal(queen), vertical(queen))

    assert sorted(queen.move_range) == sorted(queen.attack_range)
    assert sorted(exp_ranges) == sorted(queen.move_range)


@pytest.mark.parametrize("wrong_pos_coords", INVALID_MOVES)
def test_queen_incorrect_move(wrong_pos_coords, queen):  # noqa: D103
    assert not queen.move(queen.position)
    assert not queen.move(Position(*wrong_pos_coords) + queen.position)

    assert not queen.move(Position(MAX_POS, queen.position.file))
    assert not queen.move(Position(-1, queen.position.file))
    assert not queen.move(Position(queen.position.rank, MAX_POS))
    assert not queen.move(Position(queen.position.rank, -1))
