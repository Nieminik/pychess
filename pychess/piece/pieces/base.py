from collections import namedtuple

from pychess.piece.color import Color

position_tup = namedtuple("Position", "row, col")

MIN_POS = 0
MAX_POS = 8


class Piece(object):
    def __init__(self, position, color=Color.White):
        self._pos = position_tup(*position)
        self.color = color
        self.grid = None
        self.moves = 0

    @property
    def move_range(self):
        return []

    @property
    def attack_range(self):
        return self.move_range

    @property
    def position(self):
        return self._pos

    @position.setter
    def position(self, value):
        self._pos = position_tup(*value)

    def __repr__(self):
        return f"{self.color.name} {self.__class__.__name__} at {self.position}"
