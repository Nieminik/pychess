"""Tests for Queen class."""

import pytest

from pychess.grid import Grid
from pychess.piece.position import Position, MAX_POS
from pychess.piece.pieces import Queen

from pychess.piece.move_iters import diagonal, horizontal, vertical

from itertools import chain

COORDS_GROUP = (
    (1, 2),
    (2, 1),
    (0, 2),
    (7, 7)
)


@pytest.fixture
def queen():  # noqa: D103
    grid = Grid()
    queen = Queen(Position(1, 1))
    grid.add_piece(queen)
    return queen


@pytest.mark.parametrize("coords", COORDS_GROUP)
def test_queen_ranges(coords, queen):  # noqa: D103
    queen.move(coords)
    queen.grid.add_piece(queen)

    exp_ranges = chain(diagonal(queen),  horizontal(queen),  vertical(queen))

    assert sorted(queen.move_range) == sorted(queen.attack_range)
    assert sorted(exp_ranges) == sorted(queen.move_range)


def test_queen_incorrect_move(queen):  # noqa: D103
    assert not queen.move(queen.position)
    invalid_moves = [(1, 2), (1, -2), (-1, 2), (-1, -2)]
    invalid_moves += list(map(reversed, invalid_moves))

    for inv_move in invalid_moves:
        assert not queen.move(Position(*inv_move) + queen.position)

    assert not queen.move(Position(MAX_POS, queen.position.col))
    assert not queen.move(Position(-1, queen.position.col))
    assert not queen.move(Position(queen.position.row, MAX_POS))
    assert not queen.move(Position(queen.position.row, -1))
