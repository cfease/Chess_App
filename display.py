from board import FILES, RANKS

def render(board):
    print()
    for r in reversed(RANKS):
        row = []
        for f in FILES:
            piece = board.piece_at(f + r)
            row.append(str(piece) if piece else ".")
        print(r, " ".join(row))
    print("  " + " ".join(FILES))
    print()