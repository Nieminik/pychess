"""Tests for color."""

from pychess.piece.color import Color
import pytest


def test_inversion():  # noqa: D103
    assert Color.White.inverted() == Color.Black
    assert Color.Black.inverted() == Color.White


def test_inversion_wrong_cls():  # noqa: D103
    with pytest.raises(NotImplementedError):
        Color.inverted("Invalid")
