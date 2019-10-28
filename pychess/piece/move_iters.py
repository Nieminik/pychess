"""Module implementing move iterators for pieces."""
from functools import partial
from itertools import product, cycle

from pychess.piece.position import Position


def _pos_iter(piece, transformation):
    """Iterate through positions based on the given transformation function."""
    pos = piece.position
    while True:
        pos = Position(*transformation(*pos))
        if not pos.is_valid():
            break
        other_piece = piece.grid[pos]
        print("Piece: {}".format(other_piece))
        if other_piece:
            if other_piece.color != piece.color and piece.move_attacks:
                yield pos
            break
        yield pos


def _iterate_evenly(*iters, max_iters=None):
    """Conduct every given iterator one by one."""
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


def up(piece):
    """Generate up positions for given piece."""
    return _pos_iter(piece, lambda r, c: (r + 1, c))


def down(piece):
    """Generate down positions for given piece."""
    return _pos_iter(piece, lambda r, c: (r - 1, c))


def left(piece):
    """Generate left positions for given piece."""
    return _pos_iter(piece, lambda r, c: (r, c - 1))


def right(piece):
    """Generate right positions for given piece."""
    return _pos_iter(piece, lambda r, c: (r, c + 1))


def horizontal(piece, max_iters=None):
    """Generate horizontal positions for given piece."""
    return _iterate_evenly(left(piece), right(piece), max_iters=max_iters)


def vertical(piece, max_iters=None):
    """Generate vertical positions for given piece."""
    return _iterate_evenly(up(piece), down(piece), max_iters=max_iters)


def _diagonal_helper(r, c, rd, cd):
    return (r + rd, c + cd)


def diagonal(piece, max_iters=None):
    """Generate diagonal positions for given piece."""
    diffs = list(product([1, -1], repeat=2))
    funcs = (partial(_diagonal_helper, rd=rd, cd=cd) for rd, cd in diffs)
    iters = (_pos_iter(piece, func) for func in funcs)

    return _iterate_evenly(*iters, max_iters=max_iters)
