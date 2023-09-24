import os
import random
import numpy as np

def load_board():
    # Kiválasztjuk a pályát a "palyak" mappából véletlenszerűen
    palyak_path = "input/palyak/"
    available_boards = [file for file in os.listdir(palyak_path) if file.startswith("board")]
    selected_board = random.choice(available_boards)

    # Az első két szám kinyerése a pályanevből
    board_name = "_".join(selected_board.split("_")[0:3])

    with open(os.path.join(palyak_path, selected_board), "r") as f:
        board = [list(line.strip()) for line in f.readlines()]

    return selected_board, board_name, board

# Tesztelés
selected_board, board_name, board = load_board()
print(f"Selected Board: {selected_board}")
print(f"Board Name: {board_name}")
for row in board:
    print("".join(row))

def load_items(board_name):
    # Elemkészlet keresése az "items" mappában, ami a megfelelő mintával kezdődik
    items_path = "input/elemek/"

    # Kinyerjük a board_name-ből az adatokat
    board_parts = board_name.split("_")
    if len(board_parts) != 3 or board_parts[0] != "board":
        raise ValueError("Hibás board_name formátum. Példa helyes formátumra: 'board_7_8'")

    board_size = (int(board_parts[1]), int(board_parts[2]))

    matching_items = [file for file in os.listdir(items_path) if
                      file.startswith(f"items_{board_size[0]}_{board_size[1]}") and file.endswith(".txt")]

    if matching_items:
        # Véletlenszerűen válasszunk egy elemkészletet az egyezők közül
        item_set_name = random.choice(matching_items)
    else:
        item_set_name = None
    print(item_set_name)

    if item_set_name:
        with open(os.path.join(items_path, item_set_name), "r") as f:
            item_set = []
            current_letter = None

            for line in f.readlines():
                line = line.strip()

                if len(line) == 1 and line != 'o':
                    # Ha egy sor 1 karakterből áll, ami nem 'o', akkor ez egy betű
                    current_letter = line
                    collecting_oo = True
                    oo_lines = []
                elif collecting_oo and not line.startswith('-'):
                    # Ha gyűjtjük az 'oo'-kat, és a sor nem '---', akkor hozzáadjuk a sorokat az 'oo_lines'-hoz
                    line = line.replace('o', current_letter)
                    oo_lines.append(line)
                    #print(current_letter, ":")
                    #print(oo_lines)

                elif collecting_oo and line.startswith('-'):
                    # Ha a sor '---', akkor befejezzük az 'oo'-k gyűjtését
                    item_set.append(oo_lines)
                    added_rotate(item_set)
                    collecting_oo = False
        return item_set
    return None


def added_rotate(item_set):
    for i in range(len(item_set)):
        first_item = item_set[i]

        # Ellenőrizzük, hogy first_item üres-e vagy tartalmaz-e elemet
        if first_item and len(first_item) > 0:
            element_count = len(first_item)
            character_length = len(first_item[0])

            character = first_item[0][0]

            new_element_count = character_length
            new_character_length = element_count

            rotate_array = []

            # Az elem hozzáadása a tömbhöz a megfelelő számú alkalommal, kivéve, ha az element_count és character_length egyenlő
            if element_count != character_length:
                for _ in range(new_element_count):
                    rotate_array.append(character * new_character_length)
    item_set.append(rotate_array)
    return item_set

def remove_empty(item_set):
    return [item for item in item_set if item and len(item) > 0]

# Formázás és tesztelés
selected_item_set = load_items(board_name)
selected_item_set = added_rotate(selected_item_set)
selected_item_set = remove_empty(selected_item_set)
selected_item_set.pop()
if selected_item_set:
    for item in selected_item_set:
        # print('\n'.join(item))
        print("Ez egy elem:", item)
else:
    print("Nincs egyező elemkészlet.")

def place_items(board, items):
    # Számoljuk meg az elemek területét és rendezzük őket csökkenő sorrendbe
    sorted_items = sorted(items[1:], key=lambda x: sum(row.count('o') for row in x), reverse=True)

    # Kezdetben nincsenek lépések
    steps = 0

    for item in sorted_items:
        placed = False
        best_placement = None
        best_score = float('inf')

        for row in range(len(board) - len(item) + 1):
            for col in range(len(board[0]) - len(item[0]) + 1):
                can_place = True
                score = 0

                for i in range(len(item)):
                    for j in range(len(item[0])):
                        if item[i][j] == 'o':
                            if board[row + i][col + j] == 'b':
                                can_place = False
                                break
                        elif item[i][j] not in ['a', 'b']:
                            if board[row + i][col + j] != item[i][j]:
                                can_place = False
                                break
                        elif item[i][j] == 'a' and board[row + i][col + j] == '1':
                            score += 1
                            if score > best_score:
                                can_place = False
                                break

                    if not can_place:
                        break

                if can_place:
                    if score < best_score:
                        best_placement = (row, col)
                        best_score = score

        if best_placement is not None:
            row, col = best_placement
            for i in range(len(item)):
                for j in range(len(item[0])):
                    if item[i][j] == 'o':
                        board[row + i][col + j] = 'b'
                    elif item[i][j] not in ['a', 'b']:
                        board[row + i][col + j] = item[i][j]
            placed = True
            steps += 1

    return steps

def print_board(board, steps):
    # Kiírjuk a pályát és a lépésszámot
    print(f"Lépésszám: {steps}")
    for row in board:
        print("".join(row))

#def load_board_and_solve():
  #  board_size = (7, 8)  # Például, itt állítsd be a pálya méretét
    #selected_board, board_name = load_board()
    #items = load_items(board_name)

    # Inicializáljuk a pályát
   # board = [['o' for _ in range(board_size[1])] for _ in range(board_size[0])]

   # steps = place_items(board, items)

    #print_board(board, steps)

   # return board_name, board


# Tesztelés
#load_board_and_solve()
