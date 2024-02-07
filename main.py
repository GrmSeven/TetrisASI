'''
Info
A & D for moving sideways
S for mucing down
Q & E for rotating
W for dropping
'''

import os
import time
import random
from copy import deepcopy
import tkinter
from tkinter import Canvas
import keyboard

class Tetris:
    def __init__(self):
        # Constants
        self.shapes = []
        self.size = [10, 20]
        self.square_size = 40
        # Yes
        self.matrix = [[0] * (self.size[0]) for i in range(self.size[1])]
        self.prev_matrix = deepcopy(self.matrix)
        self.curr_tetromino = []
        self.tetromino_position = [0, 0]
        self.curr_color = 1
        # Ticking
        self.timer = time.time()
        self.tick = 0
        self.is_next_tick = True
        # Game state
        self.skip_next_frame = False
        self.score = 0
        self.state = 1
        self.move_vector = None  # [-1, 0]

    def pause(self):
        self.state = 0

    def unpause(self):
        self.state = 1

    def exit(self):
        self.state = -1

    def reset(self):
        # Constants
        self.shapes = []
        self.size = [10, 20]
        self.square_size = 40
        # Yes
        self.matrix = [[0] * (self.size[0]) for i in range(self.size[1])]
        self.prev_matrix = deepcopy(self.matrix)
        self.curr_tetromino = []
        self.tetromino_position = [0, 0]
        self.curr_color = 1
        # Ticking
        self.timer = time.time()
        self.tick = 0
        self.is_next_tick = True
        # Game state
        self.skip_next_frame = False
        self.score = 0
        self.state = 1
        self.move_vector = None  # [-1, 0]

    def update_timer(self, delta):
        if self.state == 1:
            if time.time() - self.timer >= delta:
                self.timer = time.time()
                self.tick += 1
                if self.skip_next_frame:
                    self.skip_next_frame = False
                else:
                    self.is_next_tick = True
            else:
                self.is_next_tick = False
        if self.state == 0:
            self.is_next_tick = False

    def add_new_shape(self, *params):
        self.shapes.append([*params])
        return len(self.shapes) - 1

    def forgor_new_shape(self, index):
        return self.shapes.pop(index)

    def clear_console(self):
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')

    def decide_next_tetromino(self):
        tetremino_params = random.choices(game.shapes, [i[1] for i in game.shapes], k=1)[0]
        self.curr_tetromino = tetremino_params[0]
        self.curr_color = tetremino_params[2]
        self.tetromino_position = [(self.size[0] // 2) - (len(self.curr_tetromino) // 2), 0]

    def draw_tetromino(self, delete=False):
        for y, row in enumerate(self.curr_tetromino):
            for x, cell in enumerate(row):
                if cell != 0:
                    self.matrix[self.tetromino_position[1] + y][self.tetromino_position[0] + x] = 0 if delete else self.curr_color

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

    def drop_tetromino(self):
        while self.move_tetromino('D'):
            self.skip_next_frame = True
            pass

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

    def check_row(self):
        checked_range = range(max(self.tetromino_position[1], 0),
                              min(self.tetromino_position[1] + len(self.curr_tetromino), self.size[1]))
        for row in checked_range:
            if all(self.matrix[row]):
                self.matrix.insert(0, [0] * self.size[0])
                self.matrix.pop(row + 1)
                self.score += 100


    def draw_square(self, x, y, color):
        s = self.square_size
        canvas.create_rectangle(x*s, y*s, x*s+s, y*s+s, fill=color, outline="")

    def render(self, render_all=False):
        cell_icon = ["#000000", "#64c9d3", "#445aa5", "#ecae35", "#eae742", "#5fbc52", "#8c5da5", "#e94138"]
        self.clear_console()
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                if render_all or self.matrix[y][x] != self.prev_matrix[y][x]:
                    self.draw_square(x, y, cell_icon[cell])
        canvas.update()
        self.prev_matrix = deepcopy(self.matrix)

    def show_score(self):
        s = self.square_size
        canvas.create_rectangle(1*s, 6*s, 8*s+s, 11*s+s, fill="#f74f43", outline="")
        canvas.create_text(200, 320, text=f"Game Over\n  Score:", font=("Terminal", 40, "bold"))
        canvas.create_text(200, 420, text=self.score, font=("Terminal", 40, "bold"), anchor=tkinter.CENTER)
        canvas.create_rectangle(200-110, 530-30, 200+110, 530+30, fill="#000000", outline="")
        canvas.create_text(200, 530, text="Press  Space\n to restart", font=("Terminal", 20, "bold"), fill="#ffffff", anchor=tkinter.CENTER)

    def print_debug(self):
        print(self.curr_tetromino)
        print(self.tetromino_position)

def create_game():
    global game
    game = Tetris()
    for tetromino in initial_tetrominos:
        game.add_new_shape(*tetromino)
    game.decide_next_tetromino()
    game.render(True)

if __name__ == "__main__":
    # Tkinter canvas
    root = tkinter.Tk()
    canvas = Canvas(root)
    canvas.pack()
    canvas.config(width=400, height=800)

    # Tetris initialisation
    initial_tetrominos = [
        [[[0, 1, 0],           #   |*|
          [1, 1, 1],           # |*|*|*|
          [0, 1, 0]], 0.8, 6], #   |*|

        [[[0, 0, 0],           #
          [1, 1, 0],           # |*|*|
          [0, 1, 0]], 1.1, 5], #   |*|

        [[[0, 0, 0],           #
          [1, 1, 1],           # |*|*|*|
          [1, 1, 1]], 1, 7],   # |*|*|*|

        [[[0, 1, 0],           #   |*|
          [1, 1, 1],           # |*|*|*|
          [1, 0, 0]], 1, 3],   # |*|

        [[[0, 1, 0, 0],        #   |*|
          [0, 1, 0, 0],        #   |*|
          [0, 1, 0, 0],        #   |*|
          [0, 1, 0, 0]], 1, 1],#   |*|

        [[[1, 1, 0],           # |*|*|
          [0, 1, 0],           #   |*|
          [1, 1, 1]], 0.8, 2], # |*|*|*|

        [[[1, 1, 1],           # |*|*|*|
          [1, 0, 1],           # |*| |*|
          [0, 0, 0]], 1, 4]    #
    ]
    create_game()

    def input_set(x):
        global next_input
        next_input = x

    keyboard.add_hotkey('a', lambda: input_set('a'))
    keyboard.add_hotkey('d', lambda: input_set('d'))
    keyboard.add_hotkey('s', lambda: input_set('s'))
    keyboard.add_hotkey('e', lambda: input_set('e'))
    keyboard.add_hotkey('q', lambda: input_set('q'))
    keyboard.add_hotkey('w', lambda: input_set('w'))
    keyboard.add_hotkey('space', lambda: input_set('space'))
    input_commands = {'a': lambda: game.move_tetromino("L"),
                      'd': lambda: game.move_tetromino("R"),
                      's': lambda: game.move_tetromino("D"),
                      'e': lambda: game.rotate_tetromino(1),
                      'q': lambda: game.rotate_tetromino(3),
                      'w': lambda: game.drop_tetromino()}

    input_set("")
    while True:  # Game loop
        if game.state == 0 and next_input == "space":
            create_game()

        if game.state == 1:
            if next_input in ['w', 'a', 's', 'd', 'q', 'e']:
                input_commands[next_input]()
                next_input = ""
                game.draw_tetromino()
                game.render()
                game.draw_tetromino(True)
            if game.is_next_tick:
                if not game.move_tetromino('D'):
                    game.draw_tetromino()
                    game.check_row()
                    game.decide_next_tetromino()
                    if game.check_collision(game.tetromino_position, game.curr_tetromino):
                        game.show_score()
                        game.pause()
                game.draw_tetromino()
                game.render()
                game.draw_tetromino(True)
            game.update_timer(0.5)

        if game.state == -1:
            break

        canvas.update()
    root.mainloop()