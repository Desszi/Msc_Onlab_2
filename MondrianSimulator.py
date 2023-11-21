import os
import random
from itertools import product

def convert(board):
    new_board = [[str(value) for value in row] for row in board]
    return new_board

def create_random_board():
    rows = 8
    cols = 8

    num_board = [[0 for _ in range(cols)] for _ in range(rows)]

    def place_element(element):
        while True:
            row = random.randint(0, rows - 1)
            col = random.randint(0, cols - 1)
            orientation = random.choice(['horizontal', 'vertical'])
            if can_place_element(num_board, row, col, element, orientation):
                place_element_at(num_board, row, col, element, orientation)
                break

    place_element(1)
    place_element(2)
    place_element(3)

    num_start_board = [row.copy() for row in num_board]

    num_board = [[0, 0, 0, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 1, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 1, 1, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

    num_start_board = [[0, 0, 0, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 1, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 1, 1, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

    board = convert(num_board)
    start_board = convert(num_start_board)

    board_name = f"board_{rows}_{cols}"
    return board_name, board, start_board

def can_place_element(board, row, col, element, orientation):
    if element == 1:
        return board[row][col] == 0
    elif element == 2:
        if orientation == 'horizontal' and col < len(board[0]) - 1:
            return board[row][col] == 0 and board[row][col + 1] == 0
        elif orientation == 'vertical' and row < len(board) - 1:
            return board[row][col] == 0 and board[row + 1][col] == 0
        else:
            return False
    elif element == 3:
        if orientation == 'horizontal' and col < len(board[0]) - 2:
            return all(board[row][c] == 0 for c in range(col, col + 3))
        elif orientation == 'vertical' and row < len(board) - 2:
            return all(board[r][col] == 0 for r in range(row, row + 3))
        else:
            return False

def place_element_at(board, row, col, element, orientation):
    if element == 1:
        board[row][col] = 1
    elif element == 2:
        if orientation == 'horizontal':
            board[row][col] = 1
            board[row][col + 1] = 1
        else:
            board[row][col] = 1
            board[row + 1][col] = 1
    elif element == 3:
        if orientation == 'horizontal':
            for c in range(col, col + 3):
                board[row][c] = 1
        else:
            for r in range(row, row + 3):
                board[r][col] = 1

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

#Egy széles elem legyen az első kiválasztáskor
def oneWide_order(selected_item_set):
    def is_one_wide(rect):
        return all(len(row) == 1 for row in rect) or len(rect) == 1
    def get_character(rect):
        return rect[0][0] if len(rect) == 1 else rect[0]
    def area_key(rect):
        return len(''.join(rect))

    # Kiválogatjuk az "egy széles" elemeket
    one_width_selected_item_set = [rect for rect in selected_item_set if is_one_wide(rect)]
    other_selected_item_set = [rect for rect in selected_item_set if not is_one_wide(rect)]

    # Az "egy széles" elemek rendezése azonos karakter és terület szerint
    one_width_selected_item_set.sort(key=lambda rect: (get_character(rect), -area_key(rect)))

    # A többi elem rendezése terület szerint csökkenő sorrendben
    other_selected_item_set.sort(key=area_key, reverse=True)

    # Összefésüljük a két listát
    ordered_selected_item_set = one_width_selected_item_set + other_selected_item_set
    return ordered_selected_item_set

def generate_combinations(selected_item_set):
    selected_item_set = strategy_order(selected_item_set)

    character_rows = {}
    for row in selected_item_set:
        character = row[0][0]
        if character not in character_rows:
            character_rows[character] = []
        character_rows[character].append(row)

    combinations = product(*character_rows.values())
    return list(combinations)

steps = 0
def place_data_backtrack_corrected(selected_item_set, board):
    global steps
    def can_place(x, y, piece):
        global steps
        for i in range(len(piece)):
            for j in range(len(piece[i])):
                if piece[i][j] != '0':
                    if (y + i >= len(board) or x + j >= len(board[0]) or
                       board[y + i][x + j] != '0'):
                        return False
        return True
    def place(x, y, piece):
        global steps
        for i in range(len(piece)):
            for j in range(len(piece[i])):
                if piece[i][j] != '0':
                    board[y + i][x + j] = piece[i][j]
                    #steps = steps + 1

    def remove(x, y, piece):
        global steps
        for i in range(len(piece)):
            for j in range(len(piece[i])):
                if piece[i][j] != '0':
                    board[y + i][x + j] = '0'
                    #steps = steps + 1

    def try_combination(index):
        global steps
        if index == len(selected_item_set):
            return all('0' not in row for row in board)
        piece = selected_item_set[index]
        for y in range(len(board) - len(piece) + 1):
            for x in range(len(board[0]) - len(piece[0]) + 1):
                if can_place(x, y, piece):
                    steps = steps + 1
                    place(x, y, piece)
                    if try_combination(index + 1):
                        return True
                    remove(x, y, piece)
        return False
    if try_combination(0):
        return True, board, steps
    else:
        return False, board, steps

def run_all_combinations(selected_item_set, board):
    all_combinations = generate_combinations(selected_item_set)
    successful_combinations_count = 0
    for combination in all_combinations:
        board_copy = [row[:] for row in board]
        success, modified_board, steps = place_data_backtrack_corrected(list(combination), board_copy)
        if success:
            successful_combinations_count += 1
            for row in modified_board:
                print(' '.join(row))

    if successful_combinations_count > 1:
        print("There are multiple successful combinations, so the board cannot be uniquely solved.")
    elif successful_combinations_count == 0:
        print("No successful combination found.")
    else:
        print("Exactly one successful combination found.", "Steps:", steps)

def print_board_csv(start_board, steps):

    csv_fajl_nev = 'board_game.csv'

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
    #while True:
    #    board_name, board, start_board = create_random_board()
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
    run_all_combinations(selected_item_set, board)


def save_game_to_csv(num_games):
    main()
   # for _ in range(num_games):
       # start_board, steps = main()
       # print_board_csv(start_board, steps)

# x játék létrehozása és CSV fájlba mentése
save_game_to_csv(1)