"""Tests for piece position class."""

import pytest
from pychess.piece.position import (
    Position, InvalidNotationError, InvalidPositionError)
from itertools import product

NOTATIONS_COORDS = {
    "a1": (0, 0),
    "c3": (2, 2),
    "c4": (3, 2),
    "e5": (4, 4),
    "a7": (6, 0)
}

COORDS_NOTATIONS = {v: k for k, v in NOTATIONS_COORDS.items()}

INVALID_NOTATIONS = ("02", "/3", "--", "i2", "3a", "a32", "a", "2", "")

INVALID_COORDS = ((-1, 2), (8, 1), (2, 8), (8, 8), (3, -1), (-2, -3))


@pytest.mark.parametrize("coords", COORDS_NOTATIONS)
def test_init(coords):  # noqa: D103
    p1 = Position(*coords)
    r, f = p1
    assert (r, f) == coords


@pytest.mark.parametrize("coords", COORDS_NOTATIONS)
def test_valid(coords):  # noqa: D103
    assert Position(*coords).is_valid()


@pytest.mark.parametrize("coords", INVALID_COORDS)
def test_invalid(coords):  # noqa: D103
    assert not Position(*coords).is_valid()


@pytest.mark.parametrize("notation, coords", NOTATIONS_COORDS.items())
def test_get_pos(notation, coords):  # noqa: D103
    assert Position.get_pos(notation) == Position(*coords)


@pytest.mark.parametrize("coords, notation", COORDS_NOTATIONS.items())
def test_get_notation(coords, notation):  # noqa: D103
    position = Position(*coords)
    assert position.get_notation() == notation


@pytest.mark.parametrize("notation", INVALID_NOTATIONS)
def test_invalid_get_pos(notation):  # noqa: D103
    with pytest.raises(InvalidNotationError):
        Position.get_pos(notation)


@pytest.mark.parametrize("coords", INVALID_COORDS)
def test_invalid_get_notation(coords):  # noqa: D103
    with pytest.raises(InvalidPositionError):
        Position(*coords).get_notation()


@pytest.mark.parametrize("coords", NOTATIONS_COORDS.values())
def test_add(coords):  # noqa: D103
    diffs = product(range(-2, 3), repeat=2)
    for dr, df in diffs:
        r, f = coords
        assert Position(r, f) + Position(dr, df) == (r + dr, f + df)
