"""Tests for src.grid."""
import pytest
from src.chess_grid import ChessGrid, MAX_COORD_VALUE
from src.piece.piece_base import BasePiece
from src.move_logic import MoveNotPossibleError

X_Y_VALUE = (
    (0, 0, 0xff),
    (1, 7, 0x01),
    (5, 2, 0x52)
)

INIT_NEW_FIELDS = (
    (0, 0, 1, 1),
    (1, 1, 0, 0),
    (2, 3, 0, 4)
)


@pytest.fixture
def piece():  # noqa: D103
    return BasePiece(-1, -1, -1)


@pytest.fixture
def grid():  # noqa: D103
    return ChessGrid()


def test_grid_init(grid):  # noqa: D103
    assert len(grid.fields) == MAX_COORD_VALUE

    for i in range(MAX_COORD_VALUE):
        assert len(grid.fields[i]) == MAX_COORD_VALUE


@pytest.mark.parametrize("row, col, value", X_Y_VALUE)
def test_get_item(row, col, value, grid):  # noqa: D103
    grid.fields[row][col] = value
    assert grid[row][col] == value
    assert grid[(row, col)] == value

    grid.fields[row][col] = ~value
    assert grid[row][col] == ~value
    assert grid[(row, col)] == ~value


@pytest.mark.parametrize("row, col, value", X_Y_VALUE)
def test_set_item(row, col, value, grid):  # noqa: D103
    grid[row][col] = value
    assert grid.fields[row][col] == value

    grid[(row, col)] = ~value
    assert grid.fields[row][col] == ~value

    grid[(row, col)] = value
    assert grid.fields[row][col] == value

    grid[row][col] = ~value
    assert grid.fields[row][col] == ~value


@pytest.mark.parametrize("x_init, y_init, row, col", (
    (0, 0, 1, 1),
    (1, 1, 0, 0),
    (2, 3, 0, 4)
))
def test_grid_move(x_init, y_init, row, col, grid, piece):  # noqa: D103
    piece._row, piece._col = (x_init, y_init)
    grid[(x_init, y_init)] = piece

    grid.move((x_init, y_init), (row, col))

    assert piece.moves == 1
    assert grid[(x_init, y_init)] is None
    assert grid[(row, col)] is piece


def test_grid_move_same_pos(grid, piece):  # noqa: D103
    field = (0, 0)
    piece._row, piece._col = field
    grid[field] = piece
    with pytest.raises(MoveNotPossibleError):
        grid.move(field, field)

    assert piece.moves == 0


@pytest.mark.parametrize("row, col", (
    (1, 1),
    (5, 4),
    (7, 7)
))
def test_erase(row, col, grid, mocker):  # noqa: D103
    fake_piece = mocker.MagicMock()
    fake_piece.row, fake_piece.col = row, col
    grid[(row, col)] = fake_piece

    grid.erase((row, col))
    assert grid[(row, col)] is None
