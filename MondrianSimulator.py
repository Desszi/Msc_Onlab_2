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

    with open(os.path.join(palyak_path, selected_board), "r") as f:
        start_board = [list(line.strip()) for line in f.readlines()]

    return selected_board, board_name, board, start_board

# Tesztelés
selected_board, board_name, board, start_board = load_board()
print(f"Selected Board: {selected_board}")
print(f"Board Name: {board_name}")
board.pop()
start_board.pop()
for row in start_board:
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

#Itt lehet majd felsorolni a stratégiákat, hogy milyen logika szerint szeretnénk letenni az elemeket
def strategy_order(selected_item_set):
    # A tömböket a méretük szerint csökkenő sorrendbe rendezzük
    selected_item_set.sort(key=lambda x: len(''.join(x)), reverse=True)
    return selected_item_set


def place_item(selected_item_set, board, row_idx=0):
    sorted_items = strategy_order(selected_item_set)
    steps = 0
    def is_placed(x, y, sorted_items):
        for i in range(len(sorted_items)):
            for j in range(len(sorted_items[i])):
                if sorted_items[i][j] != '0' and (y + i >= len(board) or x + j >= len(board[0]) or board[y + i][x + j] != '0'):
                    return False
        return True

    def take_item(x, y, sorted_items):
        for i in range(len(sorted_items)):
            for j in range(len(sorted_items[i])):
                if sorted_items[i][j] != '0':
                    board[y + i][x + j] = item[i][j]


    while row_idx < len(sorted_items):
        item = sorted_items[row_idx]
        placed = False
        for y in range(len(board) - len(item) + 1):
            for x in range(len(board[0]) - len(item[0]) + 1):
                if is_placed(x, y, item):
                    take_item(x, y, item)
                    placed = True
                    break
            if placed:
                steps += 1
                break

        # Ha sikerült elhelyezni vagy páros indexű sor volt, akkor lépjünk tovább a következő páratlan indexre.
        if placed or row_idx % 2 == 1:
            row_idx += 2 if row_idx % 2 == 0 else 1
        else:
            # Ha nem sikerült elhelyezni, lépjünk tovább a következő páros indexre.
            row_idx += 1
    return steps

steps = place_item(selected_item_set, board)

for row in board:
    print(' '.join(row))

print(f"Lépésszám: {steps}")


#Itt majd ki fogjuk írni a kezdeti pályát a megoldást és a lépésszámot, amiból később a kezdeti pályát és a lépésszámot egy csv filebe fogjuk rakni
def print_board(board, steps):
    # Kiírjuk a pályát és a lépésszámot
    print(f"Lépésszám: {steps}")
    for row in board:
        print("".join(row))


