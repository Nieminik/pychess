"""Module containing move logic related functionality."""


class MoveNotPossibleError(Exception):
    """Move not possible exception."""


def is_move_possible(o_field, n_field):
    """Determine if a move is possible."""
    return o_field != n_field  # TODO: IMPLEMENT
