"""Provide color functionality."""
from enum import Enum, auto


class Color(Enum):
    """Enum Color class."""

    White = auto()
    Black = auto()

    def inverted(self):
        """Return the oposite color."""
        cls = {Color.White.name: Color.Black,
               Color.Black.name: Color.White}.get(self.name, None)
        if cls is None:
            raise NotImplementedError
        return cls
