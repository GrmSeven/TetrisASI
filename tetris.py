import random
import os
import time
from copy import deepcopy
from pynput import keyboard


shapes = [
    [[0, 1, 0],
     [1, 1, 1],
     [0, 1, 0]],

    [[0, 0, 0],
     [0, 1, 1],
     [0, 1, 0]],

    [[0, 0, 0],
     [1, 1, 1],
     [1, 1, 1]],

    [[0, 1, 0],
     [1, 1, 1],
     [1, 0, 0]],

    [[0, 0, 1, 0],
     [0, 0, 1, 0],
     [0, 0, 1, 0],
     [0, 0, 1, 0]],

    [[1, 1, 0],
     [0, 1, 0],
     [1, 1, 1]],

    [[1, 1, 1],
     [1, 0, 1],
     [0, 0, 0]],
]


# On windows use 'cls' instead of 'clear'
def clear_console(): return os.system('clear')


def rotate_block(clockwise, block):
    """
    Rotate the given block clockwise or counterclockwise.

    Parameters:
        clockwise (bool): If True, rotate clockwise; otherwise, rotate counterclockwise.
        block (list): The 2D matrix representing the Tetris block.

    Returns:
        list: The rotated block.
    """
    if clockwise:
        return [list(row[::-1]) for row in zip(*block)]
    else:
        return [list(row) for row in zip(*block[::-1])]


game_matrix = [[0]*10]*20


tetromino = shapes[random.randint(0, 6)]
height = len(tetromino)
width = len(tetromino[0])
row_level = 0

RUN = True
HIT = False
last_game_matrix = game_matrix.copy()


# Decided to stick with pynput, because some OSes require admin permissions
def on_press(key):
    check_key(key)


def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener, just in case
        return False


def check_key(key):
    # TODO: tetrominos don't rotate in the console, even tho this returns a correct rotated tetromino, it might have to do something with this running in a separate Thread
    if key is keyboard.Key.up:
        print("up")
        tetromino = rotate_block(clockwise=False, block=tetromino)
    if key is keyboard.Key.down:
        print("down")

        tetromino = rotate_block(clockwise=True, block=tetromino)


listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()


while RUN:  # gameloop
    # handle gameboard change
    """
        Build the tetromino to the gameboard

        Returns:
            a modified game matrix

    """
    for tetromino_idx, level in enumerate(range(row_level, row_level+height)):
        if level > 18:
            HIT = True
            break

        row = game_matrix[level].copy()

        index = 0
        # indexes to be changed: 10-width/2 + width of the tetromino block + 10-width/2
        # TODO: add a possibility to move the tetromino left/right
        for cell in range((10-width)//2):

            row[index] = 0
            index += 1
            if game_matrix[level + 1][index] == 1:
                HIT = True
                break

        for x in range(height):

            row[index] = tetromino[tetromino_idx][x]
            index += 1
            if game_matrix[level + 1][index] == 1:
                HIT = True
                break

        for cell in range((10-width)//2):

            row[index] = 0
            index += 1
            print(index)
            if game_matrix[level + 1][index-1] == 1:

                HIT = True
                break

        game_matrix[level] = row

        if HIT:
            break

    # render the current game board
    for level, row in enumerate(game_matrix):
        for idx, cell in enumerate(row):
            if cell == 0:
                print(".", end="")
            else:
                print("*", end="")
        print()

    row_level += 1

    # if the current tetromino has a solid block (1) below it, it has to stop falling (or it's the bottom of the game board)
    # TODO: blocks don't align properly, bottom row get's deleted for some reason
    if HIT:
        last_game_matrix = deepcopy(game_matrix)
        HIT = False

        tetromino = shapes[random.randint(0, 6)]
        height = len(tetromino)
        width = len(tetromino[0])
        row_level = 0

    time.sleep(0.3)
    # TODO: replace it with tick based or with delta-time approach

    # instead of altering positions on the board, I will calculate block's new position every iteration and
    # before each I will replace game board with the last matrix ( that may or not have blocks there already, depending how far into the game the player got )
    game_matrix = deepcopy(last_game_matrix)

    clear_console()
