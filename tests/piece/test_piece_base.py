"""Tests for base piece."""
import pytest

from pychess.piece.pieces.base import Piece
from pychess.piece.position import Position


@pytest.fixture
def piece():  # noqa: D103
    return Piece(Position(1, 2))


def test_init(piece):  # noqa: D103
    assert isinstance(piece.position, Position)
    assert piece.moves == 0
    assert piece.grid is None


def test_move(piece):  # noqa: D103
    r, c = piece.position
    moves = piece.moves

    piece.move(Position(r, c))
    assert piece.moves == moves

    piece.move(Position(r ^ 1, c ^ 1))
    assert piece.moves == moves + 1

    piece.move(Position(r, c))
    assert piece.moves == moves + 2
