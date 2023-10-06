import csv
import os
import random
import numpy as np
import random

def create_random_board():
    rows = random.randint(6, 8)
    cols = random.randint(6, 8)

    matrix = [[random.choices([0, 1], weights=[0.75, 0.25])[0] for _ in range(cols)] for _ in range(rows)]

    board = [list(map(int, row)) for row in matrix]
    start_board = [row.copy() for row in board]

    board_name = f"board_{rows}_{cols}"
    return board_name, board, start_board


"""
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
"""
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


#Itt lehet majd felsorolni a stratégiákat, hogy milyen logika szerint szeretnénk letenni az elemeket
def strategy_order(selected_item_set):
    # A tömböket a méretük szerint csökkenő sorrendbe rendezzük
    selected_item_set.sort(key=lambda x: len(''.join(x)), reverse=True)
    return selected_item_set


def place_items(selected_item_set, board, board_name):
    sorted_items = strategy_order(selected_item_set)
    def is_placed(x, y, item, placed):
        hidden_zeros = 0
        for i in range(len(item)):
            for j in range(len(item[i])):
                # Ellenőrizzük az ütközéseket
                if item[i][j] != '0' and (y + i >= len(board) or x + j >= len(board[0]) or board[y + i][x + j] != '0'):
                    return False, 0
                # Számoljuk az alakzat által takart '0' karaktereket
                elif item[i][j] == '0' and board[y + i][x + j] == '0':
                    hidden_zeros += 1

        # Ha az alakzat karaktere már szerepel az elhelyezett listában, akkor az alakzatot nem szabad elhelyezni
        if any(char in placed for char in ''.join(item)):
            return False, 0
        return True, hidden_zeros

    def take_place(x, y, item):
        for i in range(len(item)):
            for j in range(len(item[i])):
                if item[i][j] != '0':
                    board[y + i][x + j] = item[i][j]

    is_placed_array = []
    steps = 0
    for item in sorted_items:
        best_x = best_y = -1
        most_zeros = -1
        for y in range(len(board) - len(item) + 1):
            for x in range(len(board[0]) - len(item[0]) + 1):
                takeit, hidden_zeros = is_placed(x, y, item, is_placed_array)
                steps += 1
                if takeit and hidden_zeros > most_zeros:
                    most_zeros = hidden_zeros
                    best_x = x
                    best_y = y

        # Ha találtunk jó pozíciót az alakzathoz, akkor helyezzük el és jegyezzük meg az elhelyezett karaktereket
        if best_x != -1 and best_y != -1:
            take_place(best_x, best_y, item)
            is_placed_array.extend([char for char in ''.join(item) if char != '0'])

    return steps


#Itt majd ki fogjuk írni a kezdeti pályát a megoldást és a lépésszámot, amiból később a kezdeti pályát és a lépésszámot egy csv filebe fogjuk rakni

def print_board_csv(start_board, steps):
    # CSV fájl neve
    # CSV fájl neve
    csv_fajl_nev = 'board_game.csv'

    # A játéktábla és lépésszám összefűzése egy listába
    data = [",".join(map(str, row)) for row in start_board]  # Sorok vesszővel választva

    # Az adatok írása a CSV fájlba
    with open(csv_fajl_nev, mode='a', newline='') as file:
        if os.path.exists(csv_fajl_nev):
            file.write('"')
            file.write('\n'.join(data))  # Sorokat idézőjelek között vesszővel elválasztva írjuk
            file.write('",')
            file.write(str(steps))  # Lépésszám hozzáadása
            file.write('\n')

def main():
    # Példa egy véletlenszerű méretű mátrix létrehozására
    board_name, board, start_board = create_random_board()
    print(f"Selected Board:")
    for row in start_board:
        print(row)
    print(f"Board Name: {board_name}")

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

    # Futtatjuk a kódot
    steps = place_items(selected_item_set, board, board_name)

    # Eredmény kiírása
    #for row in start_board:
    #    print(row)

    for row in board:
        print(row)
    print(f"Lerakási kísérletek száma: {steps}")

    return start_board, steps

def save_game_to_csv(num_games):
    for _ in range(num_games):
        start_board, steps = main()
        print_board_csv(start_board, steps)

# x játék létrehozása és CSV fájlba mentése
save_game_to_csv(100)
