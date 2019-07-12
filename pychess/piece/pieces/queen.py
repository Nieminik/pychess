from pychess.piece.pieces.bishop import Bishop
from pychess.piece.pieces.rook import Rook


class Queen(Bishop, Rook):
    @property
    def move_range(self):
        return super(Queen, self).move_range
