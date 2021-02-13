"""Tests for Pawn class."""

import pytest

from pychess.grid import Grid
from pychess.piece.position import Position
import pychess.piece.pieces as pieces
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
    pawn = pieces.Pawn(Position(1, 1))
    grid.add_piece(pawn)
    return pawn


def get_expected_move_range(pawn, two_positions=False):
    """Get expected move range."""
    r, f = pawn.position
    dir_val = pieces.Pawn.get_direction(pawn).value
    expected = [Position(r + dir_val, f)]
    if two_positions:
        expected.append(Position(r + dir_val * 2, f))
    return expected


def get_expected_attack_range(pawn, left=True, right=True):
    """Get expected move range."""
    r, f = pawn.position
    dir_val = pieces.Pawn.get_direction(pawn).value
    left_right = []
    if right:
        left_right.append(1)
    if left:
        left_right.append(-1)

    return [Position(r + dir_val, f + x) for x in left_right]


@pytest.mark.parametrize("r, f, color", PAWN_RANGE_TEST_DATA)
def test_pawn_move_range(r, f, color, pawn):  # noqa: D103
    pawn._pos = Position(r, f)
    pawn.color = color
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
    grid = pawn.grid
    assert pawn.move_range == get_expected_move_range(pawn, two_positions=True)

    p2 = pieces.Pawn(pawn.position + Position(1, 0), pawn.color)
    grid.add_piece(p2)
    assert pawn.move_range == []

    assert grid.move(p2.position, p2.position + Position(1, 0))
    assert pawn.move_range == get_expected_move_range(pawn, False)

    assert grid.move(p2.position, p2.position + Position(1, 0))
    assert pawn.move_range == get_expected_move_range(pawn, True)

    pawn.moves += 1
    assert pawn.move_range == get_expected_move_range(pawn, False)

    p3 = pieces.Pawn(pawn.position + Position(2, 0), pawn.color.inverted())
    grid.add_piece(p3)
    assert pawn.move_range == get_expected_move_range(pawn, False)

    assert grid.move(p3.position, p3.position + Position(-1, 0))
    assert pawn.move_range == []


def test_attack_range(pawn):  # noqa: D103
    dir_val = pawn.get_direction(pawn).value
    grid = pawn.grid

    assert pawn.attack_range == get_expected_attack_range(
        pawn, left=True, right=True)

    p2_pos = pawn.position + Position(dir_val, -1)
    grid.add_piece(pieces.Pawn(p2_pos, pawn.color))
    assert pawn.attack_range == get_expected_attack_range(
        pawn, left=False, right=True)

    p3_pos = pawn.position + Position(dir_val, 1)
    grid.add_piece(pieces.Pawn(p3_pos, pawn.color))
    assert pawn.attack_range == get_expected_attack_range(
        pawn, left=False, right=False)

    grid[p2_pos].color = grid[p2_pos].color.inverted()
    assert pawn.attack_range == get_expected_attack_range(
        pawn, left=True, right=False)

    grid[p3_pos].color = grid[p3_pos].color.inverted()
    assert pawn.attack_range == get_expected_attack_range(
        pawn, left=True, right=True)


def test_attack_range_invalid_pos(pawn):  # noqa: D103
    pawn._pos = Position(0, 0)
    assert pawn.attack_range == [(1, 1)]

    pawn._pos = Position(0, 7)
    assert pawn.attack_range == [(1, 6)]


def test_capture_not_possible(pawn):  # noqa: D103
    assert not pawn.move(pawn.position + Position(1, 1))


def test_an_passant(pawn):  # noqa: D103
    grid = pawn.grid

    p2_pos = pawn.position + Position(0, -1)
    grid.add_piece(pieces.Pawn(p2_pos, pawn.color))
    grid[p2_pos].moves = 1
    assert pawn.attack_range == get_expected_attack_range(
        pawn, left=True, right=True)

    grid[p2_pos].color = pawn.color.inverted()
    assert pawn.attack_range == get_expected_attack_range(
        pawn, left=True, right=True)

    grid[p2_pos].moves = 0
    assert pawn.attack_range == get_expected_attack_range(
        pawn, left=True, right=True)

    p3_pos = pawn.position + Position(0, 1)
    attacked_pos = p3_pos + Position(pawn.get_direction(pawn).value, 0)
    grid.add_piece(pieces.Pawn(p3_pos, pawn.color.inverted()))
    grid[p3_pos].moves = 1

    other = grid[p3_pos]
    assert grid.move(pawn.position, attacked_pos)
    assert grid.captured == [other]
