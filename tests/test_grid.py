"""Tests for grid."""

import pytest
from copy import deepcopy
from pychess.grid import Grid, Side
from pychess.piece.pieces.base import Piece
from pychess.piece.position import Position
import pychess.piece.pieces as piece_types
from pychess.piece.color import Color


@pytest.fixture
def grid():  # noqa: D103
    return Grid()


@pytest.fixture
def grid_castle():  # noqa: D103
    grid = Grid()
    setup = {
        Color.White: {
            "a1": piece_types.Rook,
            "h1": piece_types.Rook, "e1": piece_types.King
        },
        Color.Black: {
            "a8": piece_types.Rook,
            "h8": piece_types.Rook, "e8": piece_types.King
        }
    }
    for color, notations in setup.items():
        for notation, piece_cls in notations.items():
            piece = piece_cls(Position.get_pos(notation), color)
            grid.add_piece(piece)

    return grid


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


@ pytest.mark.parametrize("pieces_params", pieces_enemies_params)
def test_enemies(grid, pieces_params):  # noqa: D103
    _enemies_test_helper(grid, pieces_params, True)


@ pytest.mark.parametrize("pieces_params", pieces_no_enemies_params)
def test_no_enemies(grid, pieces_params):  # noqa: D103
    _enemies_test_helper(grid, pieces_params, False)


def test_access_field(grid, mocker):  # noqa: D103
    piece_mock = mocker.MagicMock()
    piece_mock.position = (1, 1)
    grid.add_piece(piece_mock)

    assert grid[(1, 1)] == piece_mock
    assert grid[(0, 0)] is None


def test_move(grid, mocker):  # noqa: D103
    piece_mock = mocker.MagicMock()
    piece_mock.position = (1, 1)

    grid.add_piece(piece_mock)
    grid.move((1, 1), (1, 2))

    piece_mock.move.assert_called_once_with((1, 2))
    piece_mock.position = (1, 2)

    assert grid[(1, 1)] is None
    assert grid[(1, 2)] == piece_mock


def test_captured(grid, mocker):  # noqa: D103
    piece_mock = mocker.MagicMock()
    piece_mock2 = mocker.MagicMock()

    piece_mock.position = (1, 1)
    piece_mock2.position = (1, 2)

    grid.add_piece(piece_mock)
    grid.add_piece(piece_mock2)

    grid.move((1, 1), (1, 2))

    assert grid.captured == [piece_mock2]
    assert piece_mock2 not in grid.fields.values()

    grid.report_capture(piece_mock)
    assert grid.captured == [piece_mock2, piece_mock]
    assert piece_mock not in grid.fields.values()


def test_in_check(grid):  # noqa: D103
    king = piece_types.King(Position(0, 0))
    rook = piece_types.Rook(Position(0, 1), Color.Black)

    assert not grid.own_king_in_check(king)

    grid.add_piece(king)
    grid.add_piece(rook)
    assert grid.own_king_in_check(king)

    grid.report_capture(rook)
    assert not grid.own_king_in_check(king)


def test_castle_once(grid_castle):  # noqa: D103
    grid = grid_castle
    grid2 = deepcopy(grid)

    assert grid.castle(color=Color.White, side=Side.Kingside)
    assert not grid.castle(color=Color.White, side=Side.Queenside)

    assert grid2.castle(color=Color.White, side=Side.Queenside)
    assert not grid2.castle(color=Color.White, side=Side.Kingside)


@ pytest.mark.parametrize("color", (Color.White, Color.Black))
@ pytest.mark.parametrize("file_letter", "bcdfg")
def test_castle_piece_between(color, file_letter, grid_castle):  # noqa: D103
    rank = 1 if color is Color.White else 8

    side = Side.Queenside if file_letter in "bcd" else Side.Kingside

    pawn = piece_types.Pawn(
        Position.get_pos(f"{file_letter}{rank}"), color=color.White)
    grid_castle.add_piece(pawn)

    assert not grid_castle.castle(color, side)


@ pytest.mark.parametrize("color", (Color.White, Color.Black))
@ pytest.mark.parametrize("side", (Side.Kingside, Side.Queenside))
@ pytest.mark.parametrize("p_type", (piece_types.King, piece_types.Rook))
def test_castle_moved(color, side, p_type, grid_castle):  # noqa: D103
    pieces = grid_castle._pieces[p_type]
    pieces = filter(lambda p: p.color == color, pieces)

    piece = next(pieces)

    # in case of a rook and kingside test, we want to skip the first rook
    if piece.position.file == 0 and side is Side.Kingside:
        piece = next(pieces)

    pos = piece.position
    piece.move(pos + Position(0, 1))
    piece.move(pos + Position(0, -1))
    piece.move(pos)

    assert not grid_castle.castle(color, side)

    while piece.moves:
        piece.revert_move()

    assert grid_castle.castle(color, side)


@ pytest.mark.parametrize("color", (Color.White, Color.Black))
@ pytest.mark.parametrize("side", (Side.Kingside, Side.Queenside))
def test_castle_attacking_bishop(color, side, grid_castle):  # noqa: D103
    kings = grid_castle._pieces[piece_types.King]
    king = next(filter(lambda p: p.color == color, kings))
    direction = 1 if color is Color.White else -1

    bishop = piece_types.Bishop(
        king.position + Position(direction, 0), color.inverted())

    grid_castle.add_piece(bishop)
    assert not grid_castle.castle(color, side)


def test_grid_eq(grid_castle):  # noqa: D103
    g2 = deepcopy(grid_castle)
    assert grid_castle == g2

    g2.report_capture(next(iter(g2.fields.values())))
    assert grid_castle != g2


def test_revert_move(grid):  # noqa: D103
    grids = []
    p1 = piece_types.Pawn(Position.get_pos("a2"))
    p2 = piece_types.Pawn(Position.get_pos("b2"))
    grid.add_piece(p1)
    grid.add_piece(p2)

    assert not grid.revert_move()

    grid.move(p1.position, p1.position + Position(2, 0))
    grids.append(deepcopy(grid))
    grid.move(p2.position, p2.position + Position(1, 0))
    grids.append(deepcopy(grid))
    grid.move(p1.position, p1.position + Position(1, 0))
    grids.append(deepcopy(grid))
    grid.move(p2.position, p2.position + Position(1, 0))

    assert grids[-1] != grid

    while grids:
        snapshot = grids.pop()
        assert grid.revert_move()
        assert grid == snapshot


@pytest.mark.parametrize("color", (Color.White, Color.Black))
def test_move_king_attacked_fields(color, grid):  # noqa: D103
    king = piece_types.King(Position(1, 1))
    king.color = color
    grid.add_piece(king)

    start_pos = king.position

    rook = piece_types.Rook(
        king.position + Position(2, 1),
        color=color.inverted())
    grid.add_piece(rook)

    move_pos = king.position + Position(0, 1)
    assert not grid.move(king.position, move_pos)

    rook.color = rook.color.inverted()
    assert grid.move(king.position, move_pos)

    rook.color = rook.color.inverted()
    assert grid.own_king_in_check(king)
    assert grid.move(king.position, start_pos)

    bishop = piece_types.Bishop(
        king.position + Position(0, 1),
        color=color.inverted())
    grid.add_piece(bishop)

    move_pos = start_pos + Position(-1, 0)
    assert not grid.move(king.position, move_pos)
    assert not grid.move(king.position, bishop.position)
    assert grid.move(king.position, bishop.position + Position(-1, 0))

    bishop.color = bishop.color.inverted()
    assert grid.move(king.position, move_pos)
    assert grid.move(king.position, start_pos)

    grid.report_capture(rook)
    bishop.color = bishop.color.inverted()
    assert grid.move(king.position, bishop.position)


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

    assert not grid.move(
        p2.position, p2.position + Position(1, 0))

    assert grid.move(
        p1.position, p1.position + Position(1, 0))
    assert not grid.own_king_in_check(king)

    p1.position += Position(-1, 0)

    print(king, p2, rook)
    assert grid.own_king_in_check(king)
    assert grid.move(p2.position, rook.position)

    assert not grid.own_king_in_check(king)
