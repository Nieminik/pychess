# noqa: D100

from pychess.starting_grid import get_starting_grid
from pprint import pprint


if __name__ == "__main__":
    pprint(get_starting_grid().fields)
