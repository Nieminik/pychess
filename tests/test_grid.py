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


@pytest.mark.parametrize("x, y, value", x_y_value)
def test_get_item(x, y, value, grid):  # noqa: D103
    grid.fields[x][y] = value
    assert grid[x][y] == value
    assert grid[(x, y)] == value

    grid.fields[x][y] = ~value
    assert grid[x][y] == ~value
    assert grid[(x, y)] == ~value


@pytest.mark.parametrize("x, y, value", x_y_value)
def test_set_item(x, y, value, grid):  # noqa: D103
    grid[x][y] = value
    assert grid.fields[x][y] == value

    grid[(x, y)] = ~value
    assert grid.fields[x][y] == ~value

    grid[(x, y)] = value
    assert grid.fields[x][y] == value

    grid[x][y] = ~value
    assert grid.fields[x][y] == ~value


@pytest.mark.parametrize("x_init, y_init, x, y", (
    (0, 0, 1, 1),
    (1, 1, 0, 0),
    (2, 3, 0, 4)
))
def test_move(x_init, y_init, x, y, grid, mocker):  # noqa: D103
    fake_piece = mocker.MagicMock()
    fake_piece.x, fake_piece.y = x_init, y_init
    grid[(x_init, y_init)] = fake_piece

    grid.move((x_init, y_init), (x, y))

    assert grid[(x_init, y_init)] is None
    assert grid[(x, y)] is fake_piece


@pytest.mark.parametrize("x, y", (
    (1, 1),
    (5, 4),
    (7, 7)
))
def test_erase(x, y, grid, mocker):  # noqa: D103
    fake_piece = mocker.MagicMock()
    fake_piece.x, fake_piece.y = x, y
    grid[(x, y)] = fake_piece

    grid.erase((x, y))
    assert grid[(x, y)] is None
