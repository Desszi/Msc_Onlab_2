import numpy as np
import pandas as pd
import random

# Függvény a pálya inicializálásához
def initialize_board():
    board = np.zeros((8, 8), dtype=int)
    return board

# Függvény az 1 egység hosszú elemek lerakásához
def place_single_units(board, num_units):
    for _ in range(num_units):
        row, col = random.randint(0, 7), random.randint(0, 7)
        while board[row, col] != 0:
            row, col = random.randint(0, 7), random.randint(0, 7)
        board[row, col] = 1

# Függvény a területek méretének generálásához
def generate_areas(num_areas):
    areas = []
    for _ in range(num_areas):
        area_size = random.randint(1, 8)
        areas.append(area_size)
    return sorted(areas, reverse=True)

# Függvény az elemek lerakásához a stratégiának megfelelően
def place_elements(board, areas):
    for area_size in areas:
        for row in range(8 - area_size + 1):
            for col in range(8 - area_size + 1):
                if np.all(board[row:row + area_size, col:col + area_size] == 0):
                    board[row:row + area_size, col:col + area_size] = 1
                    break


# Fő függvény a játék szimulációjához
def play_mondrian_game():
    board = initialize_board()
    place_single_units(board, 8)
    areas = generate_areas(8)
    place_elements(board, areas)
    return board

# Függvény a játék CSV fájlba mentéséhez
def save_game_to_csv(filename, num_games):
    data = []
    for _ in range(num_games):
        board = play_mondrian_game()
        num_moves = np.sum(board)
        data.append((board, num_moves))

    df = pd.DataFrame(data, columns=['Board', 'NumMoves'])
    df.to_csv(filename, index=False)


# 100 játék létrehozása és CSV fájlba mentése
save_game_to_csv('mondrian_games.csv', 100)
