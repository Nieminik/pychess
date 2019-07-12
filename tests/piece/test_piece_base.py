import pytest

from pychess.piece.pieces.base import Piece, position_tup


def test_init():
    piece = Piece((1, 1))

    assert isinstance(piece.position, position_tup)
    assert piece.moves == 0
    assert piece.grid is None
