
class Grid(object):
    def __init__(self):
        self.fields = {}

    def __getitem__(self, item):
        return self.fields.get(item, None)

    def add_piece(self, piece):
        piece.grid = self
        self.fields[piece.position] = piece
