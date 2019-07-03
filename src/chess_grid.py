"""Module implementing chess grid."""
from src.move_logic import is_move_possible, MoveNotPossibleError


MAX_COORD_VALUE = 8


class ChessGrid(object):
    """Class implementing chess grid."""

    def __init__(self):
        self.fields = [[None] * MAX_COORD_VALUE] * MAX_COORD_VALUE

    def __getitem__(self, i):
        """Use to access a field in a 8x8 grid."""
        try:
            row, col = i
            return self.fields[row][col]
        except TypeError:
            return self.fields[i]

    def __setitem__(self, i, value):
        """Use to set field in a 8x8 grid."""
        row, col = i
        self.fields[row][col] = value

    def move(self, old_field, field):
        """Move the content of one field to another."""
        if not is_move_possible(old_field, field):
            raise MoveNotPossibleError("Could not move!")

        self[old_field].field = field
        self[old_field], self[field] = None, self[old_field]

    def erase(self, field):
        """Erase the field content."""
        self[field] = None
