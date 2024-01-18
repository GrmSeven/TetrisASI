import os
import time
import random

class Tetris:
    def __init__(self, size):
        # Constants
        self.shapes = []
        self.size = size
        # Yes
        self.matrix = [[0] * size[0] for i in range(size[1])]
        self.curr_tetromino = []
        self.tetromino_position = [0, 0]
        # Ticking
        self.timer = time.time()
        self.tick = 0
        self.is_next_tick = True
        # Game state
        self.state = "Running"  # Or paused

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
        os.system('cls')

    def decide_next_tetromino(self):
        self.curr_tetromino = random.choices([i[0] for i in game.shapes], [i[1] for i in game.shapes], k=1)[0]
        self.tetromino_position = [(self.size[0] // 2) - (len(self.curr_tetromino) // 2), 0]

    def render_tetromino(self, cell_type):
        for y, row in enumerate(self.curr_tetromino):
            for x, cell in enumerate(row):
                if cell != 0:
                    self.matrix[self.tetromino_position[1] + y][self.tetromino_position[0] + x] = cell_type

    def move_tetromino(self, direction):
        move_vector = {'L': [-1, 0], 'R': [1, 0], 'D': [0, 1]}
        for y, row in enumerate(self.curr_tetromino):
            for x, cell in enumerate(row):
                if cell != 0:
                    matrix_x = self.tetromino_position[0] + x + move_vector[direction][0]
                    matrix_y = self.tetromino_position[1] + y + move_vector[direction][1]
                    is_outside = (matrix_x not in range(0, self.size[0])) or \
                                 (matrix_y not in range(0, self.size[1]))
                    if is_outside:
                        return False
                    is_not_empty = self.matrix[matrix_y][matrix_x] != 0
                    if is_not_empty:
                        return False
        self.tetromino_position[0] += move_vector[direction][0]
        self.tetromino_position[1] += move_vector[direction][1]
        return True

    def render(self):
        cell_icon = ["__", "[]", "{}", "()"]
        self.clear_console()
        for y, row in enumerate(game.matrix):
            for x, cell in enumerate(row):
                print(cell_icon[cell], end="")
            print("\n", end="")

    def print_debug(self):
        print(self.curr_tetromino)
        print(self.tetromino_position)

if __name__ == "__main__":
    game = Tetris([10, 20])
    timer = 0
    initial_tetrominos = [
        [[[0, 1, 0],
          [1, 1, 1],
          [0, 1, 0]], 1],
        [[[0, 0, 0],
          [0, 1, 1],
          [0, 1, 0]],1],
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
    while True:  # Game loop
        if game.is_next_tick:
            game.render_tetromino(2)
            game.render()
            game.print_debug()
            game.render_tetromino(0)
            if not game.move_tetromino('D'):
                game.render_tetromino(1)
                game.decide_next_tetromino()
        game.update_timer(0.5)