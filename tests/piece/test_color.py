"""Tests for color."""

from pychess.piece.color import Color


def test_inversion():  # noqa: D103
    assert Color.White.inverted() == Color.Black
    assert Color.Black.inverted() == Color.White
