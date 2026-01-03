from pieces import Piece

FILES = "abcdefgh"
RANKS = "12345678"

class Board:
    def __init__(self):
        self.grid = {}
        self._setup()

    def _setup(self):
        # Pawns
        for f in FILES:
            self.grid[f + "2"] = Piece("P", "w")
            self.grid[f + "7"] = Piece("P", "b")

        # Back rank
        order = ["R", "N", "B", "Q", "K", "B", "N", "R"]
        for i, f in enumerate(FILES):
            self.grid[f + "1"] = Piece(order[i], "w")
            self.grid[f + "8"] = Piece(order[i], "b")

    def move_piece(self, move, color):
        """
        Extremely naive:
        - Finds *any* matching piece of the right type and color
        - Ignores collisions, legality, check, etc.
        """

        if move.castle:
            # Stub: ignore castling mechanics entirely
            print(f"{color} castles {move.castle}")
            return

        # Find candidate piece
        candidates = [
            sq for sq, p in self.grid.items()
            if p.kind == move.piece and p.color == color
        ]

        if not candidates:
            raise RuntimeError("No matching piece found")

        source = candidates[0]

        # Capture if present
        if move.target in self.grid:
            del self.grid[move.target]

        self.grid[move.target] = self.grid[source]
        del self.grid[source]

    def piece_at(self, square):
        return self.grid.get(square)
