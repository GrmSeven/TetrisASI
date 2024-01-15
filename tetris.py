import random
import tkinter
from tkinter import font
from tkinter import *
import random


def onKeyPress(event):
   return event.keycode


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

game_matrix = [[0]*10]*20

class Block:
    def __init__():
        x = 0
        y = 0

def draw_square(x, y, color):
    side = 50
    canvas.create_rectangle(x*side, y*side, x*side+side, y*side+side, fill=color, outline="")

def matrix_rotation(matrix, state):
    m_len = len(matrix)
    new_matrix = [[]*m_len]*m_len
    for i in range(state):
        for x in range(m_len):
            for y in range(m_len):
                new_matrix[x][y] = matrix[m_len - y - 1][x]
    return new_matrix

#  Game loop
if __name__ == "__main__":
    root = tkinter.Tk()
    canvas = Canvas(root)
    canvas.pack()
    root.geometry('1024x576')
    y = 0


    for lst in matrix_rotation(shapes[5], 1):
        x = 0
        for item in lst:
            if item == 1:
                draw_square(x, y, '#000000')
            x += 1
        y += 1

    root.bind('<KeyPress>', onKeyPress)
    root.mainloop()
