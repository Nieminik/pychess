"""Tests for base piece."""
from itertools import product

import pytest

from pychess.piece.pieces.base import Piece
from pychess.piece.position import Position, MAX_POS
from pychess.piece.color import Color
from pychess.grid import Grid
import pychess.piece.pieces as piece_types


@pytest.fixture
def piece():  # noqa: D103
    return Piece(Position(1, 2))


def test_init(piece):  # noqa: D103
    assert isinstance(piece.position, Position)
    assert piece.moves == 0
    assert piece.grid is None


def test_move(piece):  # noqa: D103
    moves = piece.moves
    start_pos = piece.position

    piece._mv_range = list(product(range(MAX_POS), repeat=2))

    assert not piece.move(piece.position)
    assert piece.moves == moves

    assert piece.move(piece.position + Position(1, 0))
    assert piece.moves == moves + 1

    piece.move(start_pos)
    assert piece.moves == moves + 2


def test_move_in_check():  # noqa: D103
    grid = Grid()
    r, f = 1, 1
    king = piece_types.King(Position(r, f - 1))
    rook = piece_types.Rook(Position(r, f + 1), color=Color.Black)
    p1 = piece_types.Pawn(Position(r - 1, f))
    p2 = piece_types.Pawn(Position(r - 1, f + 2))

    for piece in (king, rook, p1, p2):
        grid.add_piece(piece)

    assert grid.own_king_in_check(king)

    assert not p2.move(p2.position + Position(1, 0))

    assert p1.move(p1.position + Position(1, 0))
    assert not grid.own_king_in_check(king)

    p1._pos += Position(-1, 0)

    assert grid.own_king_in_check(king)
    assert grid.move(p2.position, rook.position)

    assert not grid.own_king_in_check(king)
