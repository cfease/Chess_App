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
        if move.castle:
            print(f"{color} castles {move.castle}")
            return

        # Pawn handling (minimal but correct)
        if move.piece == "P":
            target_file = move.target[0]

            candidates = [
                sq for sq, p in self.grid.items()
                if p.kind == "P"
                and p.color == color
                and sq[0] == target_file
            ]
        else:
            candidates = [
                sq for sq, p in self.grid.items()
                if p.kind == move.piece and p.color == color
            ]

        if not candidates:
            raise RuntimeError("No matching piece found")

        source = candidates[0]

        if move.target in self.grid:
            del self.grid[move.target]

        self.grid[move.target] = self.grid[source]
        del self.grid[source]

    def piece_at(self, square):
        return self.grid.get(square)
    
# --- Disambiguation helper functions ---

def square_to_coords(square):
    file, rank = square
    return FILES.index(file), RANKS.index(rank)

def can_reach(piece, source, target):
    sx, sy = square_to_coords(source)
    tx, ty = square_to_coords(target)

    dx = tx - sx
    dy = ty - sy

    if piece.kind == "N":
        return (abs(dx), abs(dy)) in {(1, 2), (2, 1)}

    if piece.kind == "B":
        return abs(dx) == abs(dy)

    if piece.kind == "R":
        return dx == 0 or dy == 0

    if piece.kind == "Q":
        return dx == 0 or dy == 0 or abs(dx) == abs(dy)

    if piece.kind == "K":
        return max(abs(dx), abs(dy)) == 1

    return False
