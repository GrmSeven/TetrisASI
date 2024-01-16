import os
import time
import random

class Tetris:
    def __init__(self, size):
        self.shapes = []
        self.size = size
        self.matrix = [[0] * size[0]] * size[1]
        self.state = "Running"  # Or paused

    def add_new_shape(self, matrix, rarity):
        self.shapes.append([matrix, rarity])
        return len(self.shapes) - 1

    def forgor_new_shape(self, index):
        return self.shapes.pop(index)

    def clear_console(self):
        os.system('cls')
        
    def render(self):
        self.clear_console()
        for y, row in enumerate(game.matrix):
            for x, cell in enumerate(row):
                if cell == 0:
                    print(".", end="")
                else:
                    print("*", end="")
            print("\n", end="")

    def test_update(self):
        self.matrix[5][2] += 1


if __name__ == "__main__":
    game = Tetris([10, 20])
    game.add_new_shape([[0, 1, 0],
                    [1, 1, 1],
                    [0, 1, 0]], 1)
    game.add_new_shape([[0, 0, 0],
                    [0, 1, 1],
                    [0, 1, 0]], 1)
    game.add_new_shape([[0, 0, 0],
                    [1, 1, 1],
                    [1, 1, 1]], 1)
    game.add_new_shape([[0, 1, 0],
                    [1, 1, 1],
                    [1, 0, 0]], 1)
    game.add_new_shape([[0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0]], 1)
    game.add_new_shape([[1, 1, 0],
                    [0, 1, 0],
                    [1, 1, 1]], 1)
    game.add_new_shape([[1, 1, 1],
                    [1, 0, 1],
                    [0, 0, 0]], 1)
    # Game loop
    while True:
        game.test_update()
        game.render()
        time.sleep(1)

