"""Tests for grid."""

import pytest
from pychess.grid import Grid
from pychess.piece.pieces.base import Piece
from pychess.piece.color import Color


@pytest.fixture
def grid():  # noqa: D103
    return Grid()


pieces_enemies_coords = (
    ((1, 2), (1, 1)),
    ((2, 3), (4, 4)),
    ((5, 5), (0, 1))
)

pieces_enemies_colors = (
    (Color.White, Color.Black),
    (Color.Black, Color.White),
    (Color.White, Color.Black)
)

pieces_no_enemies_colors = (
    (Color.White, Color.White),
    (Color.Black, Color.Black),
    (Color.White, Color.White)
)

pieces_enemies_params = zip(pieces_enemies_coords, pieces_enemies_colors)
pieces_no_enemies_params = zip(pieces_enemies_coords, pieces_no_enemies_colors)


def _enemies_test_helper(grid, pieces_params, enemies):
    pieces_params = zip(*pieces_params)
    for params in pieces_params:
        piece = Piece(*params)
        grid.add_piece(piece)
    pieces = grid.fields.values()
    assert pieces

    for piece in pieces:
        assert bool(grid.get_enemies(piece)) == enemies


def test_add_piece(grid, mocker):  # noqa: D103
    piece_mock = mocker.MagicMock()
    grid.add_piece(piece_mock)

    assert piece_mock.grid == grid


@pytest.mark.parametrize("pieces_params", pieces_enemies_params)
def test_enemies(grid, pieces_params):  # noqa: D103
    _enemies_test_helper(grid, pieces_params, True)


@pytest.mark.parametrize("pieces_params", pieces_no_enemies_params)
def test_no_enemies(grid, pieces_params):  # noqa: D103
    _enemies_test_helper(grid, pieces_params, False)
