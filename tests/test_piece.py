"""Tests for src.piece.piece_base."""
import pytest

from src.chess_grid import ChessGrid
from src.piece.piece_base import BasePiece


@pytest.fixture
def piece():  # noqa: D103
    return BasePiece(1, 2, 3, ChessGrid())


@pytest.mark.parametrize("row, col, color", (
    (0, 0, 0),
    (1, 2, 3),
    (4, 2, 1)
))
def test_piece_init(row, col, color):  # noqa: D103
    piece = BasePiece(row, col, color, ChessGrid())

    assert piece.row == row
    assert piece.col == col
    assert piece.color == color


@pytest.mark.parametrize("coord", ("row", "col"))
def test_piece_set_x_y(coord, piece, mocker):  # noqa: D103
    update_spy = mocker.patch.object(piece.grid, "move", unsafe=True)

    setattr(piece, coord, 2)

    assert getattr(piece, coord) == 2
    update_spy.assert_called()


def test_piece_get_field(piece):  # noqa: D103
    assert piece.field == (1, 2)
    assert piece.field.row == 1
    assert piece.field.col == 2


@pytest.mark.parametrize("row, col", (
    (2, 3),
    (3, 2),
    (5, 5)
))
def test_piece_set_field(row, col, piece):  # noqa: D103
    piece.field = (row, col)
    assert piece.field.row == row
    assert piece.field.col == col
    assert piece.field == (row, col)
    assert piece.row == row
    assert piece.col == col


def test_delete(piece):  # noqa: D103
    row, col = piece.field
    grid = piece.grid

    del piece

    with pytest.raises(UnboundLocalError):
        print(piece)

    assert grid[(row, col)] is None
