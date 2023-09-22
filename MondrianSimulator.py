import random
import os
def load_board_and_items():
    # Kiválasztjuk a pályát a "palyak" mappából véletlenszerűen
    palyak_path = "input/palyak/"
    available_boards = [file for file in os.listdir(palyak_path) if file.startswith("board")]
    selected_board = random.choice(available_boards)

    # Az első két szám kinyerése a pályanevből
    board_size = selected_board.split("_")[1:3]  # Az első két számot kiválasztjuk
    board_name = f"board_{board_size[0]}_{board_size[1]}"

    # Elemkészlet keresése az "items" mappában, ami a megfelelő mintával kezdődik
    items_path = "input/elemek/"
    matching_items = [file for file in os.listdir(items_path) if file.startswith(f"items_{board_size[0]}_{board_size[1]}")]

    if matching_items:
        # Ha találtunk egyező elemkészletet, válasszuk ki az elsőt
        item_set_name = matching_items[0]

        # Elemkészlet betöltése
        items_file = os.path.join(items_path, item_set_name)
        with open(items_file, "r") as f:
            item_set = [list(line.strip()) for line in f.readlines()]

        return board_name, item_set
    else:
        # Ha nem találtunk egyező elemkészletet, jelentsünk hibát vagy térjünk vissza
        raise FileNotFoundError(f"Nincs megfelelő elemlészlet ehhez a pályához: {board_name}")

def print_board(board):
    for row in board:
        print(" ".join(str(item) for item in row))


def place_items(board, item_set):
    steps = 0
    for row_idx in range(len(board)):
        for col_idx in range(len(board[row_idx])):
            if board[row_idx][col_idx] == ".":
                item = item_set.pop(0) if item_set else None
                if item:
                    board[row_idx][col_idx] = item
                    steps += 1
                else:
                    return board, steps
    return board, steps

def main():
    selected_board, item_set = load_board_and_items()
    print(f"Kiválasztott pálya: {selected_board}")

    # Inicializáljuk a pályát '.'-el, ahol '.' a még üres területet jelzi
    board_size = (len(item_set), len(item_set[0]))
    board = [["." for _ in range(board_size[1])] for _ in range(board_size[0])]

    # Elemek elhelyezése
    placed_board, steps = place_items(board, item_set)

    print("\nHozzá tartozó elemkészlet:")
    print_board(board)

    #if not item_set:
       # print("\nSolution:")
       # print_board(placed_board)
      #  print(f"\nSolved in {steps} steps.")
   # else:
      #  print("\nNo solution found.")

if __name__ == "__main__":
    main()

