from enum import Enum, auto


class Color(Enum):
    White = auto()
    Black = auto()

    def inverted(self):
        cls = {Color.White.name: Color.Black,
               Color.Black.name: Color.White}.get(self.name, None)
        if cls is None:
            raise NotImplementedError
        return cls
