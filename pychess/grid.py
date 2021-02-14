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

    def __eq__(self, other):
        eq = True
        for piece in self.fields:
            eq *= piece in other.fields

        for piece in other.fields:
            eq *= piece in self.fields

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

    def get_enemies(self, piece):
        """Get enemies of given piece."""
        inverted_color = piece.color.inverted()

        return [x for x in self.pieces if x.color is inverted_color]

    def can_move(self, old_pos, new_pos):
        """Check if king will be in check after the move."""
        piece = self[old_pos]
        other = self[new_pos]
        if other:
            self._pieces[type(other)].remove(other)
        piece._pos = new_pos

        in_check = self.own_king_in_check(piece)

        if other:
            self._pieces[type(other)].append(other)
        piece._pos = old_pos

        return not in_check

    def move(self, old_pos, new_pos):
        """Move piece."""
        piece = self[old_pos]
        other = self[new_pos]
        snapshot = deepcopy(self)

        move_successful = piece.move(new_pos)

        if other and move_successful:
            self.report_capture(other)

        if move_successful:
            self.snapshots.append(snapshot)

        return move_successful

    def report_capture(self, piece):
        """Keep track of captured pieces."""
        self.captured.append(piece)
        self._pieces[piece.__class__].remove(piece)

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
        move_pos = Position(king.position.rank, king.position.file + direction)

        if grid[move_pos] or not rook.move(move_pos):
            return False

        grid._pieces[piece_types.Rook].remove(rook)
        for i in range(2):
            moved = king.move(
                Position(king.position.rank, king.position.file + direction))
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
            snapshot = self.snapshots[-1]
        except IndexError:
            return False

        self._pieces = snapshot._pieces
        self.snapshots = snapshot.snapshots
        self.captured = snapshot.captured

        return True
