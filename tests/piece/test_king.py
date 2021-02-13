"""Tests for King class."""

import pytest

from pychess.grid import Grid
from pychess.piece.color import Color
from pychess.piece.position import Position, MAX_POS
import pychess.piece.pieces as pieces

from itertools import chain

from pychess.piece.move_iters import diagonal, horizontal, vertical


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


@pytest.mark.parametrize("wrong_pos_coords", INVALID_MOVES)
def test_king_incorrect_move(wrong_pos_coords, king):  # noqa: D103
    assert not king.move(king.position)
    assert not king.move(Position(*wrong_pos_coords) + king.position)

    assert not king.move(Position(MAX_POS, king.position.file))
    assert not king.move(Position(-1, king.position.file))
    assert not king.move(Position(king.position.rank, MAX_POS))
    assert not king.move(Position(king.position.rank, -1))


@pytest.mark.parametrize("color", (Color.White, Color.Black))
def test_king_attacked_move_fields(color, king):  # noqa: D103
    grid = king.grid
    king.color = color
    start_pos = king.position

    rook = pieces.Rook(
        king.position + Position(2, 1),
        color=color.inverted())
    grid.add_piece(rook)

    move_pos = king.position + Position(0, 1)
    assert not king.move(move_pos)

    rook.color = rook.color.inverted()
    assert king.move(move_pos)

    rook.color = rook.color.inverted()
    assert king.move(start_pos)

    bishop = pieces.Bishop(
        king.position + Position(0, 1),
        color=color.inverted())
    grid.add_piece(bishop)

    move_pos = start_pos + Position(-1, 0)
    assert not king.move(move_pos)
    assert not king.move(bishop.position)
    assert king.move(bishop.position + Position(-1, 0))

    bishop.color = bishop.color.inverted()
    assert king.move(move_pos)
    assert king.move(start_pos)

    grid.report_capture(rook)
    bishop.color = bishop.color.inverted()
    assert king.move(bishop.position)
