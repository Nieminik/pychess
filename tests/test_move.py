"""Tests for move logic module."""
import pytest
from src.move_logic import is_move_possible
from src.piece.piece_base import Field


@pytest.mark.parametrize("x, y", (
    (0, 0),
    (2, 8),
    (9, 8)
))
def test_move_possible_same_field(x, y):  # noqa: D103
    is_move_possible(Field(x, y), Field(x, y))
