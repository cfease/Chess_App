from board import Board
from notation import parse_algebraic
from display import render

def main():
    board = Board()
    turn = "w"

    while True:
        render(board)
        move_str = input(f"{'White' if turn == 'w' else 'Black'} move: ")

        if move_str.lower() in {"quit", "exit"}:
            break

        try:
            move = parse_algebraic(move_str)
            board.move_piece(move, turn)
            turn = "b" if turn == "w" else "w"
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()