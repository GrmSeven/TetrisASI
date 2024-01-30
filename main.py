import os
import time
import random
from copy import deepcopy
import tkinter
from tkinter import Canvas
import keyboard

class Tetris:
    def __init__(self, size):
        # Constants
        self.shapes = []
        self.size = size
        # Yes
        self.matrix = [[0] * (size[0]) for i in range(size[1])]
        self.prev_matrix = deepcopy(self.matrix)
        self.curr_tetromino = []
        self.tetromino_position = [0, 0]
        # Ticking
        self.timer = time.time()
        self.tick = 0
        self.is_next_tick = True
        # Game state
        self.state = "Running"  # Or paused

        self.move_vector = None  # [-1, 0]

    def update_timer(self, delta):
        if time.time() - self.timer >= delta:
            self.timer = time.time()
            self.tick += 1
            self.is_next_tick = True
        else:
            self.is_next_tick = False

    def add_new_shape(self, matrix, rarity):
        self.shapes.append([matrix, rarity])
        return len(self.shapes) - 1

    def forgor_new_shape(self, index):
        return self.shapes.pop(index)

    def clear_console(self):
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')

    def decide_next_tetromino(self):
        self.curr_tetromino = random.choices([i[0] for i in game.shapes], [i[1] for i in game.shapes], k=1)[0]
        self.tetromino_position = [(self.size[0] // 2) - (len(self.curr_tetromino) // 2), 0]

    def draw_tetromino(self, cell_type):
        for y, row in enumerate(self.curr_tetromino):
            for x, cell in enumerate(row):
                if cell != 0:
                    self.matrix[self.tetromino_position[1] + y][self.tetromino_position[0] + x] = cell_type

    def check_collision(self, pos, mat):
        for y, row in enumerate(mat):
            for x, cell in enumerate(row):
                if cell != 0:
                    matrix_x, matrix_y = pos[0] + x, pos[1] + y
                    if (matrix_x not in range(0, self.size[0])) or (matrix_y not in range(0, self.size[1])):
                        return True
                    if self.matrix[matrix_y][matrix_x] != 0:
                        return True
        return False

    def move_tetromino(self, direction):
        move_vector = {'L': [-1, 0], 'R': [1, 0], 'D': [0, 1]}

        new_pos = [self.tetromino_position[i] + move_vector[direction][i] for i in range(2)]

        if self.check_collision(new_pos, self.curr_tetromino):
            return False
        self.tetromino_position[0] += move_vector[direction][0]
        self.tetromino_position[1] += move_vector[direction][1]
        return True

    def rotate_tetromino(self, n):
        size = len(self.curr_tetromino)
        new_mat = deepcopy(self.curr_tetromino)
        for _ in range(n):
            for i in range(size):
                j = 0
                k = size - 1
                while j < k:
                    t = new_mat[j][i]
                    new_mat[j][i] = new_mat[k][i]
                    new_mat[k][i] = t
                    j += 1
                    k -= 1

            for i in range(size):
                for j in range(i, size):
                    t = new_mat[i][j]
                    new_mat[i][j] = new_mat[j][i]
                    new_mat[j][i] = t

        if self.check_collision(self.tetromino_position, new_mat):
            return False
        self.curr_tetromino = deepcopy(new_mat)
        return True

    def draw_square(self, x, y, color, size=40):
        canvas.create_rectangle(x*size, y*size, x*size+size, y*size+size, fill=color, outline="")

    def render(self, render_all=False):
        cell_icon = ["#000000", "#00ffff", "#0000ff", "#00ff00"]
        self.clear_console()
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                if render_all or self.matrix[y][x] != self.prev_matrix[y][x]:
                    self.draw_square(x, y, cell_icon[cell])
        canvas.update()
        self.prev_matrix = deepcopy(self.matrix)

    def print_debug(self):
        print(self.curr_tetromino)
        print(self.tetromino_position)

if __name__ == "__main__":
    # Tkinter canvas
    root = tkinter.Tk()
    canvas = Canvas(root)
    canvas.pack()
    canvas.config(width=400, height=800)

    # Tetris initialisation
    game = Tetris([10, 20])
    initial_tetrominos = [
        [[[0, 1, 0],
          [1, 1, 1],
          [0, 1, 0]], 1],
        [[[0, 0, 0],
          [0, 1, 1],
          [0, 1, 0]], 1],
        [[[0, 0, 0],
          [1, 1, 1],
          [1, 1, 1]], 1],
        [[[0, 1, 0],
          [1, 1, 1],
          [1, 0, 0]], 1],
        [[[0, 0, 1, 0],
          [0, 0, 1, 0],
          [0, 0, 1, 0],
          [0, 0, 1, 0]], 1],
        [[[1, 1, 0],
          [0, 1, 0],
          [1, 1, 1]], 1],
        [[[1, 1, 1],
          [1, 0, 1],
          [0, 0, 0]], 1]
    ]
    for tetromino in initial_tetrominos:
        game.add_new_shape(*tetromino)

    game.decide_next_tetromino()
    game.render(True)

    next_input = ""
    def input_add(x):
        next_input = x
        print(next_input)

    for i in ['a', 'd', 's', 'e', 'q']:
        keyboard.add_hotkey(i, lambda: input_add(i))
    input_commands = {"a": lambda: game.move_tetromino("L"),
                      "d": lambda: game.move_tetromino("R"),
                      "s": lambda: game.move_tetromino("D"),
                      "e": lambda: game.rotate_tetromino(1),
                      "q": lambda: game.rotate_tetromino(3)}

    while True:  # Game loop
        if next_input != "":
            input_commands[next_input]()
            next_input = ""
            game.draw_tetromino(2)
            game.render()
            game.draw_tetromino(0)
        if game.is_next_tick:
            if not game.move_tetromino('D'):
                game.draw_tetromino(1)
                game.decide_next_tetromino()
                if game.check_collision(game.tetromino_position, game.curr_tetromino):
                    break
            game.draw_tetromino(2)
            game.render()
            game.draw_tetromino(0)
        game.update_timer(0.5)
