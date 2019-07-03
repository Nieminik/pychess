"""Module implementing chess grid."""
from src.move_logic import is_move_possible


class GridMoveError(Exception):
    """Custom exception for move error."""


class ChessGrid(object):
    """Class implementing chess grid."""

    def __init__(self):
        self.fields = [[None] * 8] * 8

    def __getitem__(self, i):
        """Use to access a field in a 8x8 grid."""
        if hasattr(i, "__getitem__") and len(i) == 2:
            return self.fields[i[0]][i[1]]
        return self.fields[i]

    def __setitem__(self, i, value):
        """Use to set field in a 8x8 grid."""
        self.fields[i[0]][i[1]] = value

    def move(self, old_field, field):
        """Move the content of one field to another."""
        if not is_move_possible(old_field, field):
            return

        try:
            self[old_field].field = field
        except AttributeError:
            return

        self[old_field], self[field] = None, self[old_field]

    def erase(self, field):
        """Erase the field content."""
        self[field] = None