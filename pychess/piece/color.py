"""Provide color functionality."""
from enum import Enum, auto


class Color(Enum):
    """Enum Color class."""

    White = auto()
    Black = auto()

    def inverted(self):
        """Return the oposite color."""
        cls = {Color.White: Color.Black,
               Color.Black: Color.White}.get(self, None)

        if cls is None:
            raise NotImplementedError(
                f"Inversion rule was not added for given enum object: {self}")

        return cls
