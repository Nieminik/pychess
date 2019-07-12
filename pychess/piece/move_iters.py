from copy import copy
from functools import partial
from itertools import product, cycle

from pychess.piece.pieces.base import position_tup, MIN_POS, MAX_POS
from pychess.piece.color import Color
from pychess.piece.pieces.pawn import Pawn


def _pos_iter(piece, transformation):
    row, col = piece.position
    while True:
        row, col = transformation(row, col)
        if not all(map(lambda x: x in range(MIN_POS, MAX_POS), (row, col))):
            break
        other_piece = piece.grid[(row, col)]
        if other_piece:
            if other_piece.color != piece.color and not isinstance(piece, Pawn):
                yield position_tup(row, col)
            break
        yield position_tup(row, col)


def _iterate_evenly(*iters, max_iters=None):
    exclude_iters = set()
    iters = set(iters)
    for i, iter in enumerate(cycle(iters)):
        if max_iters == i:
            break

        if iter in exclude_iters:
            continue
        try:
            yield next(iter)
        except StopIteration:
            exclude_iters.add(iter)

        if not iters.difference(exclude_iters):
            break


def forward(piece):
    step = 1 if piece.color is Color.White else -1
    return _pos_iter(piece, lambda r, c: (r + step, c))


def back(piece):
    piece = copy(piece)
    piece.color = piece.color.inverted()
    return forward(piece)


def left(piece):
    return _pos_iter(piece, lambda r, c: (r, c - 1))


def right(piece):
    return _pos_iter(piece, lambda r, c: (r, c + 1))


def horizontal(piece, max_iters=None):
    return _iterate_evenly(left(piece), right(piece), max_iters=max_iters)


def vertical(piece, max_iters=None):
    return _iterate_evenly(forward(piece), back(piece), max_iters=max_iters)


def diagonal(piece, max_iters=None):
    diffs = list(product([1, -1], repeat=2))
    funcs = (partial((lambda r, c, rd, cd: (r+rd,c+cd)), rd=rd, cd=cd) for rd, cd in diffs)
    iters = (_pos_iter(piece, func) for func in funcs)

    return _iterate_evenly(*iters, max_iters=max_iters)
