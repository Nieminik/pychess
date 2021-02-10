"""Tests for King class."""

import pytest

from pychess.grid import Grid
from pychess.piece.position import Position, MAX_POS
from pychess.piece.pieces import King

from pychess.piece.move_iters import diagonal, horizontal, vertical

from itertools import chain

COORDS_GROUP = (
    (1, 2),
    (2, 1),
    (0, 2),
    (7, 7)
)

INVALID_MOVES = [(0, 2), (0, -2), (2, 0), (-2, 0), (2, 2), (-2, -2)]


@pytest.fixture
def king():  # noqa: D103
    grid = Grid()
    king = King(Position(1, 1))
    grid.add_piece(king)
    return king


@pytest.mark.parametrize("coords", COORDS_GROUP)
def test_king_ranges(coords, king):  # noqa: D103
    king.move(coords)
    king.grid.add_piece(king)

    exp_ranges = chain(
        diagonal(king, 4), horizontal(king, 2), vertical(king, 2))

    assert sorted(king.move_range) == sorted(king.attack_range)
    assert sorted(exp_ranges) == sorted(king.move_range)


@pytest.mark.parametrize("wrong_move_pos", INVALID_MOVES)
def test_king_incorrect_move(wrong_move_pos, king):  # noqa: D103
    assert not king.move(king.position)
    assert not king.move(Position(*wrong_move_pos) + king.position)

    assert not king.move(Position(MAX_POS, king.position.col))
    assert not king.move(Position(-1, king.position.col))
    assert not king.move(Position(king.position.row, MAX_POS))
    assert not king.move(Position(king.position.row, -1))
