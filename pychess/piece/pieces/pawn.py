from itertools import zip_longest

from pychess.piece.pieces.base import Piece, position_tup, MAX_POS, MIN_POS
from pychess.piece.color import Color
import pychess.piece.move_iters as m_iters


class Pawn(Piece):
    @property
    def move_range(self):
        rng = []
        fwd = m_iters.forward(self)
        for pos, move_cond in zip_longest(fwd, (True, not self.moves)):
            if pos and move_cond:
                rng.append(position_tup(*pos))

        return rng

    @property
    def attack_range(self):
        row, col = self.position
        n_row = row + (1 if self.color is Color.White else -1)
        rng = []

        for n_col in (col + 1, col - 1):
            if n_col in range(MIN_POS, MAX_POS):
                rng.append(position_tup(n_row, n_col))

        return rng
