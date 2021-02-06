"""Module implementing grid functionality."""

from itertools import chain


class Grid(object):
    """A class for containing pieces."""

    def __init__(self):  # noqa: D103
        self._pieces = {}
        self.captured = []

    def __getitem__(self, item):  # noqa: D105
        return self.fields[item]

    @property
    def pieces(self):
        return chain.from_iterable(self._pieces.values())
    
    @property
    def fields(self):
        defaultdict(lambda: None, {p.position: p for p in pieces})

    def add_piece(self, piece):
        """Add a piece to the grid."""
        piece.grid = self
        cls_pieces = self._pieces.setdefault(piece.__class__, [])
        cls_pieces.append(piece)

    def get_enemies(self, piece):
        """Get enemies of given piece."""
        inverted_color = piece.color.inverted()
        
        return [x for x in self.pieces if x.color is inverted_color]

    def move(self, old_pos, new_pos):
        """Move piece."""
        piece = self[old_pos]
        other = self[new_pos]

        move_successful = piece.move(new_pos)

        if other and move_successful:
            self.report_capture(other)

        return move_successful

    def report_capture(self, piece):
        """Keep track of captured pieces."""
        self.captured.append(piece)
        self.pieces[piece.__class__].remove(piece)
