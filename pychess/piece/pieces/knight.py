from itertools import product

from pychess.piece.pieces.base import Piece, MIN_POS, MAX_POS, position_tup


class Knight(Piece):
    @property
    def move_range(self):
        row, col = self.position
        diffs = list(product([1, -1], [2, -2]))
        diffs += [tuple(reversed(x)) for x in diffs]
        rng = []
        for d_row, d_col in diffs:
            n_row, n_col = row + d_row, col + d_col
            if n_row in range(MIN_POS, MAX_POS) and n_col in range(MIN_POS, MAX_POS):
                rng.append(position_tup(n_row, n_col))

        return rng
