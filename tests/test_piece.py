"""Tests for src.piece.piece_base."""
import pytest

from src.piece.piece_base import BasePiece


ROWS_COLS = (
    (2, 3),
    (3, 2),
    (5, 5)
)


@pytest.fixture
def piece():  # noqa: D103
    return BasePiece(-1, -1, -1)


@pytest.mark.parametrize("row, col, color", (
    (0, 0, 0),
    (1, 2, 3),
    (4, 2, 1)
))
def test_piece_init(row, col, color):  # noqa: D103
    piece = BasePiece(row, col, color)

    assert piece.row == row
    assert piece.col == col
    assert piece.color == color


@pytest.mark.parametrize("coord", ("row", "col"))
def test_piece_set_x_y(coord, piece, mocker):  # noqa: D103
    setattr(piece, coord, 2)

    assert getattr(piece.field, coord) == 2


def test_piece_get_field(piece):  # noqa: D103
    row, col = piece._row, piece._col
    assert piece.field == (row, col)
    assert piece.field.row == row
    assert piece.field.col == col


@pytest.mark.parametrize("row, col", ROWS_COLS)
def test_piece_set_field(row, col, piece):  # noqa: D103
    piece.field = (row, col)
    assert piece.field.row == row
    assert piece.field.col == col
    assert piece.field == (row, col)
    assert piece.row == row
    assert piece.col == col


@pytest.mark.parametrize("row, col", (
    (2, 3),
    (3, 2),
    (7, 1)
))
def test_piece_moves_increment(row, col, piece):  # noqa: D103
    init_moves = piece.moves
    piece.field = (row, col)
    assert piece.moves == init_moves + 1

    piece.field = (row, col)
    assert piece.moves == init_moves + 2

    piece.field = ((row + 1) % 8, col)
    assert piece.moves == init_moves + 3
