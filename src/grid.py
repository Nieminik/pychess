
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

    def move(self, old_field, field):
        self[old_field], self[field] = None, self[old_field]

    def erase(self, field):
        self[field] = None
