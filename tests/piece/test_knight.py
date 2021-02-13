"""Tests for Knight class."""

import pytest

from pychess.grid import Grid
from pychess.piece.position import Position, MAX_POS
from pychess.piece.color import Color
from itertools import product
import pychess.piece.pieces as pieces


COORDS_GROUP = (
    (1, 2),
    (2, 1),
    (0, 2),
    (7, 7)
)


INVALID_MOVES = list(product((-1, 0, 1), repeat=2))


@pytest.fixture
def knight():  # noqa: D103
    grid = Grid()
    knight = pieces.Knight(Position(1, 1))
    grid.add_piece(knight)
    return knight


@pytest.mark.parametrize("color", (Color.White, Color.Black))
@pytest.mark.parametrize("coords", COORDS_GROUP)
def test_knight_ranges(color, coords, knight):  # noqa: D103
    knight._pos = Position(*coords)
    knight.color = color

    assert sorted(knight.move_range) == sorted(knight.attack_range)

    move_diffs = [(1, 2), (1, -2), (-1, 2), (-1, -2)]
    move_diffs += list(map(reversed, move_diffs))
    move_diffs = map(lambda x: Position(*x), move_diffs)
    moves = map(lambda x: x + knight.position, move_diffs)
    moves = list(filter(lambda x: x.is_valid(), moves))
    assert sorted(knight.move_range) == sorted(moves)

    pos = knight.position + Position(1, 2)
    pawn = pieces.Pawn(pos, color=color)
    knight.grid.add_piece(pawn)

    try:
        moves.remove(pawn.position)
    except ValueError:
        pass
    assert sorted(knight.move_range) == sorted(moves)

    pawn.color = pawn.color.inverted()
    if pawn.position.is_valid():
        moves.append(pawn.position)
    assert sorted(knight.move_range) == sorted(moves)


@pytest.mark.parametrize("wrong_pos_coords", INVALID_MOVES)
def test_knight_incorrect_move(wrong_pos_coords, knight):  # noqa: D103
    assert not knight.move(knight.position)
    assert not knight.move(knight.position + Position(*wrong_pos_coords))

    assert not knight.move(Position(MAX_POS, knight.position.file))
    assert not knight.move(Position(-1, knight.position.file))
    assert not knight.move(Position(knight.position.rank, MAX_POS))
    assert not knight.move(Position(knight.position.rank, -1))
