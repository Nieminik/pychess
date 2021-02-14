"""Tests for base piece."""
from itertools import product

import pytest

from pychess.piece.pieces.base import Piece
from pychess.piece.position import Position, MAX_POS
from copy import deepcopy


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


def test_piece_eq(piece):  # noqa: D103
    other = deepcopy(piece)
    assert other == piece

    other.color = other.color.inverted()
    assert other != piece

    other = deepcopy(piece)
    other.position = other.position + Position(1, 1)
    assert other != piece


def test_revert_move(piece):  # noqa: D103
    positions = [piece.position]

    for _ in range(3):
        piece.move(piece.position + Position(1, 0))
        positions.append(piece.position)

    while positions:
        assert positions.pop() == piece.position
        piece.revert_move()
