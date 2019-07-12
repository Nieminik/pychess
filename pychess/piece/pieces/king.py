from itertools import chain

from pychess.piece.pieces.base import Piece
from pychess.piece.move_iters import horizontal, vertical, diagonal


class King(Piece):
    @property
    def move_range(self):
        hor, ver, diag = horizontal(self, 2), vertical(self, 2), diagonal(self, 4)

        pieces = [x for x in self.grid.fields.values() if x.color is self.color.inverted()]
        all_attack_range = list(chain.from_iterable([p.attack_range for p in pieces]))

        rng = [h for h in hor] + [v for v in ver] + [d for d in diag]
        return [x for x in rng if x not in all_attack_range]
