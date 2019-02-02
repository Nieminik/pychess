from src.utils.color import Color


class Field(tuple):

    def __new__(cls, x, y):
        return super(Field, cls).__new__(cls, (x, y))

    def __init__(self, x, y):
        super(Field, self).__init__()
        self.x, self.y = x, y


class BasePiece(object):

    def __init__(self, x, y, color=Color.WHITE, grid=None):
        self._x = x
        self._y = y
        self.color = color
        self.grid = grid

    def __del__(self):
        self.grid.erase(self.field)

    @property
    def field(self):
        return Field(self.x, self.y)

    @field.setter
    def field(self, value):
        self.grid.move(self.field, value)
        self._x, self._y = value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self.field = value, self.y

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self.field = self.x, value
