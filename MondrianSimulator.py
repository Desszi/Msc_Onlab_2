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
board.pop()
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

#Itt lehet majd felsorolni a stratégiákat, hogy milyen logika szerint szeretnénk letenni az elemeket
def strategy_order(selected_item_set):
    # A tömböket a méretük szerint csökkenő sorrendbe rendezzük
    selected_item_set.sort(key=lambda x: len(''.join(x)), reverse=True)
    return selected_item_set

#Egy elemet megpróbálunk lerakni a pályán
def place_item(board, item):
    for row in range(len(board) - len(item) + 1):
        for col in range(len(board[0]) - len(item[0]) + 1):
            can_place = True
            for i in range(len(item)):
                for j in range(len(item[0])):
                    if board[i][j] == 1 and board[row + i][col + j] != 0:
                        can_place = False
                        break
                if not can_place:
                    break
            if can_place:
                for i in range(len(item)):
                    for j in range(len(item[0])):
                        if board[i][j] == 0:
                            board[row + i][col + j] = item[i][j]  # Cseréljük ki az elem karakterére
                return True
    return False
def place_sorted_items(board,selected_item_set):
    sorted_items = strategy_order(selected_item_set)
    solved_board = [row[:] for row in board]  # Másolat készítése a kiinduló pályáról
    for item in sorted_items:
        placed = place_item(solved_board, item)
        if not placed:
            return None  # Nem sikerült lerakni az elemet, visszatérünk None értékkel
    return solved_board  # Visszatérünk a megoldott pályával

solved_board = place_sorted_items(board, selected_item_set)

# Eredmény kiírása
if solved_board is not None:
    for row in solved_board:
        print("Megoldott sor:", row)
else:
    print("Nem sikerült lerakni az elemeket.")

#Itt majd ki fogjuk írni a kezdeti pályát a megoldást és a lépésszámot, amiból később a kezdeti pályát és a lépésszámot egy csv filebe fogjuk rakni
def print_board(board, steps):
    # Kiírjuk a pályát és a lépésszámot
    print(f"Lépésszám: {steps}")
    for row in board:
        print("".join(row))


