"""Module implementing grid functionality."""


class Grid(object):
    """A class for containing pieces."""

    def __init__(self):  # noqa: D103
        self.fields = {}

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