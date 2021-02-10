"""Tests for King class."""

import pytest

from pychess.grid import Grid
from pychess.piece.color import Color
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

INVALID_MOVES = [(0, 2), (0, -2), (2, 0), (-2, 0), (2, 2), (-2, -2)]


@pytest.fixture
def king():  # noqa: D103
    grid = Grid()
    king = pieces.King(Position(1, 1))
    grid.add_piece(king)
    return king


@pytest.mark.parametrize("coords", COORDS_GROUP)
def test_king_ranges(coords, king):  # noqa: D103
    king._pos = Position(*coords)

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


@pytest.mark.parametrize("color", (Color.White, Color.Black))
def test_king_attacked_move_fields(color, king):  # noqa: D103
    grid = king.grid
    king.color = color

    start_move_range = set(king.move_range)

    rook = pieces.Rook(
        Position(king.position.row + 2, king.position.col + 1),
        color=color.inverted())
    grid.add_piece(rook)

    expected_range = start_move_range - set(rook.attack_range)

    assert king.move_range != king.attack_range
    assert sorted(king.move_range) == sorted(expected_range)

    rook.color = rook.color.inverted()
    assert sorted(king.move_range) != sorted(expected_range)
    rook.color = rook.color.inverted()

    bishop = pieces.Bishop(
        Position(king.position.row, king.position.col + 1),
        color=color)
    grid.add_piece(bishop)

    # bishop now blocks two fields of rook's attack range
    expected_range.add(Position(bishop.position.row - 1, bishop.position.col))
    assert sorted(king.move_range) == sorted(expected_range)

    bishop.color = bishop.color.inverted()
    expected_range = expected_range - set(bishop.attack_range)
    expected_range.add(Position(bishop.position.row, bishop.position.col))

    assert sorted(king.move_range) == sorted(expected_range)
