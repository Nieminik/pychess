"""Module implementing grid functionality."""


class Grid(object):
    """A class for containing pieces."""

    def __init__(self):  # noqa: D103
        self.fields = {}
        self.captured = []

    def __getitem__(self, item):  # noqa: D105
        return self.fields.get(item, None)

    def add_piece(self, piece):
        """Add a piece to the grid."""
        piece.grid = self
        self.fields[piece.position] = piece

    def get_enemies(self, piece):
        """Get enemies of given piece."""
        inverted_color = piece.color.inverted()
        return [x for x in self.fields.values() if x.color is inverted_color]

    def move(self, old_pos, new_pos):
        """Move piece."""
        piece = self[old_pos]
        other = self[new_pos]

        move_successful = piece.move(new_pos)

        if move_successful:
            del self.fields[old_pos]
            self.fields[new_pos] = piece

        if other and move_successful:
            self.report_capture(other)

        return move_successful

    def report_capture(self, piece):
        """Keep track of captured pieces."""
        self.captured.append(piece)
        for pos, grid_piece in dict(self.fields).items():
            if piece == grid_piece:
                del self.fields[pos]
