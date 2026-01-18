from pieces import Piece

FILES = "abcdefgh"
RANKS = "12345678"
   
# --- Disambiguation helper functions ---

def square_to_coords(square):
    file, rank = square
    return FILES.index(file), RANKS.index(rank)

def path_clear(board, source, target):
    sx, sy = square_to_coords(source)
    tx, ty = square_to_coords(target)

    dx = tx - sx
    dy = ty - sy

    step_x = (dx > 0) - (dx < 0)
    step_y = (dy > 0) - (dy < 0)

    x, y = sx + step_x, sy + step_y
    while (x, y) != (tx, ty):
        sq = FILES[x] + RANKS[y]
        if sq in board.grid:
            return False
        x += step_x
        y += step_y

    return True

def can_reach(board, piece, source, target, capture):
    sx, sy = square_to_coords(source)
    tx, ty = square_to_coords(target)

    dx = tx - sx
    dy = ty - sy

    abs_dx = abs(dx)
    abs_dy = abs(dy)

    direction = 1 if piece.color == "w" else -1
    start_rank = 1 if piece.color == "w" else 6

    # Knight
    if piece.kind == "N":
        return (abs_dx, abs_dy) in {(1, 2), (2, 1)}

    # Bishop
    if piece.kind == "B":
        return abs_dx == abs_dy and path_clear(board, source, target)

    # Rook
    if piece.kind == "R":
        return (dx == 0 or dy == 0) and path_clear(board, source, target)

    # Queen
    if piece.kind == "Q":
        return (
            (dx == 0 or dy == 0 or abs_dx == abs_dy)
            and path_clear(board, source, target)
        )

    # King
    if piece.kind == "K":
        return max(abs_dx, abs_dy) == 1

    # Pawn
    if piece.kind == "P":
        # Forward move
        if not capture:
            if dx != 0:
                return False
            if dy == direction:
                return target not in board.grid
            if sy == start_rank and dy == 2 * direction:
                intermediate = FILES[sx] + RANKS[sy + direction]
                return (
                    intermediate not in board.grid
                    and target not in board.grid
                )
            return False

        # Capture
        return abs_dx == 1 and dy == direction and target in board.grid

    return False

# --- Board class ---

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

        # Step 1: candidate pieces by type and color
        candidates = [
            sq for sq, p in self.grid.items()
            if p.kind == move.piece and p.color == color
        ]

        # Step 2: filter by pseudo-legal reachability
        candidates = [
            sq for sq in candidates
            if can_reach(self, self.grid[sq], sq, move.target, move.capture)
        ]

        # Step 3: SAN disambiguation
        if move.source_hint:
            if move.source_hint in FILES:
                candidates = [sq for sq in candidates if sq[0] == move.source_hint]
            elif move.source_hint in RANKS:
                candidates = [sq for sq in candidates if sq[1] == move.source_hint]

        if not candidates:
            raise RuntimeError("Illegal move (no valid piece can reach target)")

        if len(candidates) > 1:
            raise RuntimeError("Ambiguous move")

        source = candidates[0]

        # Capture
        if move.target in self.grid:
            del self.grid[move.target]

        self.grid[move.target] = self.grid[source]
        del self.grid[source]

    def piece_at(self, square):
        return self.grid.get(square)
 