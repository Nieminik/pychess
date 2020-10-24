"""Tests for Pawn class."""

import pytest

from pychess.grid import Grid
from pychess.piece.position import Position
from pychess.piece.pieces.pawn import Pawn
from pychess.piece.color import Color


PAWN_RANGE_TEST_DATA = (
    (1, 1, Color.White),
    (1, 2, Color.White),
    (4, 5, Color.Black),
    (5, 4, Color.Black)
)


@pytest.fixture
def pawn():  # noqa: D103
    grid = Grid()
    return Pawn(Position(1, 1), grid=grid)


@pytest.mark.parametrize("r, c, col", PAWN_RANGE_TEST_DATA)
def test_pawn_range(r, c, col, pawn):  # noqa: D103
    pawn._pos = Position(r, c)
    pawn.color = col

    dir_val = Pawn.get_direction(pawn).value
    expected_rng = [Position(r + dir_val, c),
                    Position(r + dir_val * 2, c)]
    assert pawn.move_range == expected_rng

    pawn.moves += 1
    assert pawn.move_range == [Position(r + dir_val, c)]


def test_pawn_empty_range(pawn):  # noqa: D103
    pawn._pos = Position(7, 5)
    pawn.color = Color.White
    assert pawn.move_range == []

    pawn._pos = Position(0, 5)
    pawn.color = Color.Black
    assert pawn.move_range == []


def test_pawn_range_obstruction(pawn):  # noqa: D103
    raise Exception("Test not implemented!")  # TODO: add test
