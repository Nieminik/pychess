"""Tests for src.grid."""
import pytest
from src.grid import Grid


x_y_value = (
    (0, 0, 0xff),
    (1, 7, 0x01),
    (5, 2, 0x52)
)


@pytest.fixture
def grid():  # noqa: D103
    return Grid()


def test_grid_init(grid):  # noqa: D103
    assert len(grid.fields) == 8

    for i in range(8):
        assert len(grid.fields[i]) == 8


@pytest.mark.parametrize("row, col, value", x_y_value)
def test_get_item(row, col, value, grid):  # noqa: D103
    grid.fields[row][col] = value
    assert grid[row][col] == value
    assert grid[(row, col)] == value

    grid.fields[row][col] = ~value
    assert grid[row][col] == ~value
    assert grid[(row, col)] == ~value


@pytest.mark.parametrize("row, col, value", x_y_value)
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
def test_move(x_init, y_init, row, col, grid, mocker):  # noqa: D103
    fake_piece = mocker.MagicMock()
    fake_piece.row, fake_piece.col = x_init, y_init
    grid[(x_init, y_init)] = fake_piece

    grid.move((x_init, y_init), (row, col))

    assert grid[(x_init, y_init)] is None
    assert grid[(row, col)] is fake_piece


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
