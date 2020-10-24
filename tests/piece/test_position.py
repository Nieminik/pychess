"""Tests for piece position class."""

from pychess.piece.position import Position


def test_init():  # noqa: D103
    p1 = Position(1, 2)
    r, c = p1
    assert r, c == (1, 2)


def test_translate():  # noqa: D103
    assert Position.translate_pos("a1") == (0, 0)
    assert Position.translate_pos("c3") == (2, 2)
    assert Position.translate_pos("c4") == (2, 3)


def test_get():  # noqa: D103
    p1 = Position.get_pos("b1")
    r, c = p1
    assert r, c == (1, 0)
