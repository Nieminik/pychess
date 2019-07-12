from pychess.piece.pieces.base import Piece
from pychess.piece.move_iters import horizontal, vertical


class Rook(Piece):
    @property
    def move_range(self):
        return list(horizontal(self)) + list(vertical(self)) + super(Rook, self).move_range
