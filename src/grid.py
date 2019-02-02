
class Grid:
    _grid_obj = None

    def __init__(self):
        self.fields = [[None] * 8] * 8

    def __getitem__(self, i):
        if hasattr(i, "__getitem__") and len(i) == 2:
            return self.fields[i[0]][i[1]]
        return self.fields[i]

    def __setitem__(self, i, value):
        self.fields[i[0]][i[1]] = value

    @staticmethod
    def get_grid():
        if Grid._grid_obj is None:
            Grid._grid_obj = Grid()
        return Grid._grid_obj

    def move(self, old_field, field):
        self[old_field], self[field] = None, self[old_field]

    def discard(self, field):
        self[field] = None
