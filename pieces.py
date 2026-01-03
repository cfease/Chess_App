from dataclasses import dataclass

@dataclass
class Piece:
    kind: str   # 'P', 'N', 'B', 'R', 'Q', 'K'
    color: str  # 'w' or 'b'

    def __str__(self):
        return self.kind if self.color == 'w' else self.kind.lower()