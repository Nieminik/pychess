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


def get_expected_move_range(pawn, two_positions=False):
    """Get expected move range."""
    r, c = pawn.position
    dir_val = Pawn.get_direction(pawn).value
    expected = [Position(r + dir_val, c)]
    if two_positions:
        expected.append(Position(r + dir_val * 2, c))
    return expected


def get_expected_attack_range(pawn, left=True, right=True):
    """Get expected move range."""
    r, c = pawn.position
    dir_val = Pawn.get_direction(pawn).value
    left_right = []
    if right:
        left_right.append(1)
    if left:
        left_right.append(-1)

    return [Position(r + dir_val, c + x) for x in left_right]


@pytest.mark.parametrize("r, c, col", PAWN_RANGE_TEST_DATA)
def test_pawn_move_range(r, c, col, pawn):  # noqa: D103
    pawn._pos = Position(r, c)
    pawn.color = col
    assert pawn.move_range == get_expected_move_range(pawn, True)

    pawn.moves += 1
    assert pawn.move_range == get_expected_move_range(pawn, False)


def test_pawn_empty_range(pawn):  # noqa: D103
    pawn._pos = Position(7, 5)
    pawn.color = Color.White
    assert pawn.move_range == []

    pawn._pos = Position(0, 5)
    pawn.color = Color.Black
    assert pawn.move_range == []


def test_pawn_range_obstruction(pawn):  # noqa: D103
    r, c = pawn.position
    grid = pawn.grid
    assert pawn.move_range == get_expected_move_range(pawn, two_positions=True)

    p2 = Pawn(Position(r + 1, c), pawn.color, grid)
    grid.add_piece(p2)
    assert pawn.move_range == []

    assert grid.move(Position(r + 1, c), Position(r + 2, c))
    assert pawn.move_range == get_expected_move_range(pawn, False)

    assert grid.move(Position(r + 2, c), Position(r + 3, c))
    assert pawn.move_range == get_expected_move_range(pawn, True)

    pawn.moves += 1
    assert pawn.move_range == get_expected_move_range(pawn, False)

    p3 = Pawn(Position(r + 2, c), pawn.color.inverted(), grid)
    grid.add_piece(p3)
    assert pawn.move_range == get_expected_move_range(pawn, False)

    assert grid.move(p3.position, (r + 1, c))
    assert pawn.move_range == []


def test_attack_range(pawn):  # noqa: D103
    r, c = pawn.position
    dir_val = pawn.get_direction(pawn).value
    grid = pawn.grid

    assert pawn.attack_range == get_expected_attack_range(pawn)

    p2_pos = Position(r + dir_val, c - 1)
    grid.add_piece(Pawn(p2_pos))
    assert pawn.attack_range == get_expected_attack_range(
        pawn, left=False, right=True)

    p3_pos = Position(r + dir_val, c + 1)
    grid.add_piece(Pawn(p3_pos))
    assert pawn.attack_range == get_expected_attack_range(
        pawn, left=False, right=False)

    grid[p2_pos].color = grid[p2_pos].color.inverted()
    assert pawn.attack_range == get_expected_attack_range(
        pawn, left=True, right=False)

    grid[p3_pos].color = grid[p3_pos].color.inverted()
    assert pawn.attack_range == get_expected_attack_range(
        pawn, left=True, right=True)
