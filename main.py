import os
import time
import random

class Tetris:
    def __init__(self, size):
        self.shapes = []
        self.size = size
        self.matrix = [[0] * size[0] for i in range(size[1])]
        self.timer = time.time()
        self.state = "Running"  # Or paused

    def update_timer(self, delta):
        if time.time() - self.timer >= delta:
            self.timer = time.time()
            return 1
        return 0

    def add_new_shape(self, matrix, rarity):
        self.shapes.append([matrix, rarity])
        return len(self.shapes) - 1

    def forgor_new_shape(self, index):
        return self.shapes.pop(index)

    def clear_console(self):
        os.system('cls')
        
    def render(self):
        cell_icon = ["   ", "[.]"]
        self.clear_console()
        for y, row in enumerate(game.matrix):
            for x, cell in enumerate(row):
                print(cell_icon[cell], end="")
            print("\n", end="")


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
        print(tetromino)
        game.add_new_shape(*tetromino)

    # Game loop
    while True:
        if game.update_timer(1):
            game.matrix[random.randint(0, game.size[1]-1)][random.randint(0, game.size[0]-1)] = 1
            game.render()