"""Tests for src.piece.piece_base."""
import pytest

from src.grid import Grid
from src.piece.piece_base import BasePiece


@pytest.fixture
def piece():  # noqa: D103
    return BasePiece(1, 2, 3, Grid())


@pytest.mark.parametrize("x, y, color", (
    (0, 0, 0),
    (1, 2, 3),
    (4, 2, 1)
))
def test_piece_init(x, y, color):  # noqa: D103
    piece = BasePiece(x, y, color, Grid())

    assert piece.x == x
    assert piece.y == y
    assert piece.color == color


@pytest.mark.parametrize("coord", ("x", "y"))
def test_piece_set_x_y(coord, piece, mocker):  # noqa: D103
    update_spy = mocker.patch.object(piece.grid, "move", unsafe=True)

    setattr(piece, coord, 2)

    assert getattr(piece, coord) == 2
    update_spy.assert_called()


def test_piece_get_field(piece):  # noqa: D103
    assert piece.field == (1, 2)
    assert piece.field.x == 1
    assert piece.field.y == 2


@pytest.mark.parametrize("x, y", (
    (2, 3),
    (3, 2),
    (5, 5)
))
def test_piece_set_field(x, y, piece):  # noqa: D103
    piece.field = (x, y)
    assert piece.field.x == x
    assert piece.field.y == y
    assert piece.field == (x, y)
    assert piece.x == x
    assert piece.y == y


def test_delete(piece):  # noqa: D103
    x, y = piece.field
    grid = piece.grid

    del piece

    with pytest.raises(UnboundLocalError):
        print(piece)

    assert grid[(x, y)] is None
