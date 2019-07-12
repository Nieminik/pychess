from pychess.piece.pieces.base import Piece
from pychess.piece.move_iters import diagonal


class Bishop(Piece):
    @property
    def move_range(self):
        return list(diagonal(self)) + super(Bishop, self).move_range
