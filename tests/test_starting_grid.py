"""Tests for starting grid."""

from pychess.piece.position import Position
from pychess.starting_grid import get_starting_grid, STARTING_NOTATIONS


def test_get_starting_grid():  # noqa: D103
    g = get_starting_grid()

    for piece_notations in STARTING_NOTATIONS.values():
        for piece_type, notations in piece_notations.items():
            for notation in notations:
                assert isinstance(
                    g.fields[Position.get_pos(notation)], piece_type)
