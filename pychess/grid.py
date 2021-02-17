"""Module implementing grid functionality."""

import math

from copy import deepcopy

from itertools import chain
from collections import defaultdict

from pychess.piece.position import Position
import pychess.piece.pieces as piece_types

from enum import Enum, auto


class Side(Enum):  # noqa: D101
    Kingside = auto()
    Queenside = auto()


class Grid(object):
    """A class for containing pieces."""

    def __init__(self):  # noqa: D103
        self._pieces = {}
        self.captured = []
        self.snapshots = []

    def __getitem__(self, item):  # noqa: D105
        return self.fields[item]

    def __deepcopy__(self, memo):  # noqa: D105
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def __eq__(self, other):  # noqa: D105
        eq = True
        for piece in self.pieces:
            eq *= piece in other.pieces

        for piece in other.pieces:
            eq *= piece in self.pieces

        return eq

    @property
    def pieces(self):  # noqa: D102
        return chain.from_iterable(self._pieces.values())

    @property
    def fields(self):  # noqa: D102
        return defaultdict(lambda: None, {p.position: p for p in self.pieces})

    def add_piece(self, piece):
        """Add a piece to the grid."""
        piece.grid = self
        cls_pieces = self._pieces.setdefault(piece.__class__, [])
        cls_pieces.append(piece)

        if piece in self.captured:
            self.captured.remove(piece)

    def get_enemies(self, piece):
        """Get enemies of given piece."""
        inverted_color = piece.color.inverted()

        return [x for x in self.pieces if x.color is inverted_color]

    def move(self, old_pos, new_pos):
        """Move piece."""
        piece = self[old_pos]
        other = self[new_pos]
        snapshot = deepcopy(self)

        move_successful = piece.move(new_pos)

        removed = other and move_successful and self.report_capture(other)

        in_check = self.own_king_in_check(piece)
        if move_successful and in_check:
            piece.revert_move()
            move_successful = False
            if removed:
                self.add_piece(other)

        if move_successful:
            self.snapshots.append(snapshot)

        return move_successful

    def report_capture(self, piece):
        """Keep track of captured pieces."""
        self.captured.append(piece)
        self._pieces[piece.__class__].remove(piece)
        return True

    def castle(self, color, side=Side.Kingside):
        """Perform a castle."""
        grid = deepcopy(self)
        king = next(
            (x for x in grid._pieces[piece_types.King] if x.color is color)
        )

        rook_f = 7 if side is Side.Kingside else 0
        rook = grid.fields[Position(king.position.rank, rook_f)]

        if not rook or not isinstance(rook, piece_types.Rook):
            return False

        if king.moves or rook.moves:
            return False

        direction = int(math.copysign(1, rook_f - king.position.file))
        move_pos = king.position + Position(0, direction)

        if grid[move_pos] or not self.move(rook.position, move_pos):
            return False

        grid._pieces[piece_types.Rook].remove(rook)
        for i in range(2):
            moved = grid.move(
                king.position, king.position + Position(0, direction))
            if not moved:
                return False

        grid._pieces[piece_types.Rook].append(rook)

        self._pieces = grid._pieces
        return True

    def own_king_in_check(self, piece):
        """Check if king of piece's color is in check right now."""
        k = next(filter(
            lambda p: p.color == piece.color,
            self._pieces.get(piece_types.King, [])), None)

        if k:
            enemies = self.get_enemies(k)
            attacks = list(
                chain.from_iterable([e.attack_range for e in enemies]))
            return k.position in attacks
        return False

    def revert_move(self):
        """Revert one move."""
        try:
            snapshot = self.snapshots.pop()
        except IndexError:
            return False

        self._pieces = snapshot._pieces
        self.captured = snapshot.captured

        return True
