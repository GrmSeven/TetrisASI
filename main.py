'''
Info
A & D - liikuda külgsuunas
S     - liikuda alla 1 võrra
Q & E - pöörelda
W     - liikuda alla
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
        # Konstandid
        self.tetrominod = []
        self.suurus = [10, 20]
        self.ruut_suurus = 48

        # Mäng
        self.maatriks = [[0] * (self.suurus[0]) for i in range(self.suurus[1])]
        self.eelmine_maatriks = deepcopy(self.maatriks)
        self.praegune_tetromino = []
        self.tetromino_positsioon = [0, 0]
        self.praegune_varv = 1

        # Taimer
        self.taimer = time.time()
        self.tick = 0
        self.on_jargmine_tick = True

        # Mängu olek
        self.jata_vahele = False  # Jääb vahele 1 tick
        self.skoor = 0
        self.olek = 1  # 1 - töötab; 0 - pausinud; 3 - lahku välja
        self.suuna_vektor = None

    # Peatab mängu
    def peata(self):
        self.olek = 0

    # Jätkab mängu
    def jatka(self):
        self.olek = 1

    # Paneb mängu kinni
    def valja(self):
        self.olek = -1

    # Kontrollib tick-i kiirus
    def uuenda_taimer(self, delta):
        if self.olek == 1:
            if time.time() - self.taimer >= delta:
                self.taimer = time.time()
                self.tick += 1
                if self.jata_vahele:
                    self.jata_vahele = False
                else:
                    self.on_jargmine_tick = True
            else:
                self.on_jargmine_tick = False
        if self.olek == 0:
            self.on_jargmine_tick = False

    # Salvestab tetrominod [kujund, tõenäosus, värv]
    def lisa_uus_kuju(self, *parameetrid):
        self.tetrominod.append([*parameetrid])
        return len(self.tetrominod) - 1

    # Kustutab tetromino mälust
    def unusta_kuju(self, index):
        return self.tetrominod.pop(index)

    # Valib järgmine kujund, nende tõenäosuse järgi
    def otsusta_jargmine_tetromino(self):
        tetremino_parameetrid = random.choices(tetris.tetrominod, [i[1] for i in tetris.tetrominod], k=1)[0]
        self.praegune_tetromino = tetremino_parameetrid[0]
        self.praegune_varv = tetremino_parameetrid[2]
        self.tetromino_positsioon = [(self.suurus[0] // 2) - (len(self.praegune_tetromino) // 2), 0]

    # Salvestab tetromino matriksile, kasutades positsioon, värv ja teised parameetrid
    def kuva_tetromino(self, kustuta=False):
        for y, rida in enumerate(self.praegune_tetromino):
            for x, piksel in enumerate(rida):
                if piksel != 0:
                    self.maatriks[self.tetromino_positsioon[1] + y][self.tetromino_positsioon[0] + x] = 0 if kustuta else self.praegune_varv

    # Vaatab kas praegune kujund põrkub milleliga matriksil
    def kontrolli_kokkuporget(self, pos, mat):
        for y, rida in enumerate(mat):
            for x, piksel in enumerate(rida):
                if piksel != 0:
                    maatriks_x, maatriks_y = pos[0] + x, pos[1] + y
                    if (maatriks_x not in range(0, self.suurus[0])) or (maatriks_y not in range(0, self.suurus[1])):
                        return True
                    if self.maatriks[maatriks_y][maatriks_x] != 0:
                        return True
        return False

    # Liigub selle vasakule, paremale või alla
    def liigu_tetromino(self, suund):
        suuna_vektor = {'L': [-1, 0], 'R': [1, 0], 'D': [0, 1]}

        uus_pos = [self.tetromino_positsioon[i] + suuna_vektor[suund][i] for i in range(2)]

        if self.kontrolli_kokkuporget(uus_pos, self.praegune_tetromino):
            return False
        self.tetromino_positsioon[0] += suuna_vektor[suund][0]
        self.tetromino_positsioon[1] += suuna_vektor[suund][1]
        return True

    # Liigub alla kuni kokkupõrkeni
    def lange_tetromino(self):
        while self.liigu_tetromino('D'):
            self.jata_vahele = True
            pass

    # Pöörab kujundi matriksi päripäeva n korda (optimeeritud viis)
    def poora_tetromino(self, n):
        suurus = len(self.praegune_tetromino)
        uus_mat = deepcopy(self.praegune_tetromino)
        for _ in range(n):
            for i in range(suurus):
                j = 0
                k = suurus - 1
                while j < k:
                    t = uus_mat[j][i]
                    uus_mat[j][i] = uus_mat[k][i]
                    uus_mat[k][i] = t
                    j += 1
                    k -= 1

            for i in range(suurus):
                for j in range(i, suurus):
                    t = uus_mat[i][j]
                    uus_mat[i][j] = uus_mat[j][i]
                    uus_mat[j][i] = t

        if self.kontrolli_kokkuporget(self.tetromino_positsioon, uus_mat):
            return False
        self.praegune_tetromino = deepcopy(uus_mat)
        return True

    # Vaatab kas ridas kõik plokid on täidetud
    def kontrolli_rida(self):
        kontrollitud_vahemik = range(max(self.tetromino_positsioon[1], 0),
                              min(self.tetromino_positsioon[1] + len(self.praegune_tetromino), self.suurus[1]))
        for rida in kontrollitud_vahemik:
            if all(self.maatriks[rida]):
                self.maatriks.insert(0, [0] * self.suurus[0])
                self.maatriks.pop(rida + 1)
                self.skoor += 100

    # Joonistab tahvlil 2d ruutu
    def draw_ruut(self, x, y, varv):
        s = self.ruut_suurus
        if varv == "#000000":
            tahvel.create_rectangle(x * s, y * s, x * s + s, y * s + s, fill=varv, outline="")
        else:
            coords = [([0, 0, 0.25, 0.25, 0.75, 0.25, 1, 0], 70),  # Ülemine
                      ([0, 1, 0.25, 0.75, 0.75, 0.75, 1, 1], -50),  # All
                      ([1, 1, 0.75, 0.75, 0.75, 0.25, 1, 0], -30),  # Parem
                      ([0, 1, 0.25, 0.75, 0.25, 0.25, 0, 0], 35),  # Vasak
                      ([0.25, 0.75, 0.25, 0.25, 0.75, 0.25, 0.75, 0.75], 0)]  # Tsenter
            for poly, varvikullastus in coords:
                toon = hex_to_rgb(varv)
                toon = (clamp(i + varvikullastus, 0, 255) for i in toon)
                toon = rgb_to_hex(toon)
                tahvel.create_polygon([(v + (x if i%2==0 else y))*s for i, v in enumerate(poly)], outline='', fill=toon)

    # Joonistab matriks (ainult muudatusi)
    def render(self, render_koik=False):
        piksel_icon = ["#000000", "#64c9d3", "#445aa5", "#ecae35", "#eae742", "#5fbc52", "#8c5da5", "#e94138"]
        for y, rida in enumerate(self.maatriks):
            for x, piksel in enumerate(rida):
                if render_koik or self.maatriks[y][x] != self.eelmine_maatriks[y][x]:
                    self.draw_ruut(x, y, piksel_icon[piksel])
        tahvel.update()
        self.eelmine_maatriks = deepcopy(self.maatriks)

    # Näitab lõpp skoor ekraanil
    def naita_skoor(self):
        s = self.ruut_suurus
        tahvel.create_rectangle(5*s-150, 10*s-90, 5*s+150, 10*s+90, fill="#f74f43", outline="")
        tahvel.create_text(5*s, 10*s-30, text=f"Game Over\n  Score:", font=("Terminal", 30, "bold"))
        tahvel.create_text(5*s, 10*s+50, text=self.skoor, font=("Terminal", 30, "bold"), anchor=tkinter.CENTER)
        tahvel.create_rectangle(5*s-120, 14*s-30, 5*s+120, 14*s+30, fill="#000000", outline="")
        tahvel.create_text(5*s, 14*s, text="Press  Space\n to restart", font=("Terminal", 20, "bold"), fill="#ffffff", anchor=tkinter.CENTER)

    def print_debug(self):
        print(self.praegune_tetromino)
        print(self.tetromino_positsioon)

def clamp(vaartus, mn, mx):
    return max(mn, min(mx, vaartus))

def hex_to_rgb(hex):
    h = hex.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def rgb_to_hex(a):
    r, g, b = a
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

# Kiiresti sättib kõik asjad et alustada mängu algusest
def loo_tetris():
    global tetris
    tetris = Tetris()
    for tetromino in esialgsed_tetrominod:
        tetris.lisa_uus_kuju(*tetromino)
    tetris.otsusta_jargmine_tetromino()
    tetris.render(True)

if __name__ == "__main__":
    # Tkinter tahvel
    raam = tkinter.Tk()
    tahvel = Canvas(raam)
    tahvel.pack()

    esialgsed_tetrominod = [
        [[[0, 1, 0],           #   |*|
          [1, 1, 1],           # |*|*|*|
          [0, 1, 0]], 0.8, 6], #   |*|

        [[[1, 1],              # |*|*|
          [0, 1]], 1.1, 5],    #   |*|

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

    # esialgsed_tetrominod = [
    #     [[[0, 0, 0, 0],
    #       [1, 1, 1, 1],
    #       [0, 0, 0, 0],
    #       [0, 0, 0, 0]], 1, 1],
    #     [[[1, 0, 0],
    #       [1, 1, 1],
    #       [0, 0, 0]], 1, 2],
    #     [[[0, 0, 1],
    #       [1, 1, 1],
    #       [0, 0, 0]], 1, 3],
    #     [[[1, 1],
    #       [1, 1]], 1, 4],
    #     [[[0, 1, 1],
    #       [1, 1, 0],
    #       [0, 0, 0]], 1, 5],
    #     [[[0, 1, 0],
    #       [1, 1, 1],
    #       [0, 0, 0]], 1, 6],
    #     [[[1, 1, 0],
    #       [0, 1, 1],
    #       [0, 0, 0]], 1, 7]
    # ]

    loo_tetris()
    tahvel.config(width=tetris.suurus[0] * tetris.ruut_suurus, height=tetris.suurus[1] * tetris.ruut_suurus)

    # Kuulab keyboard moodul ja käivitab funktsioonid
    def input_set(x):
        global jarg_input
        jarg_input = x

    keyboard.add_hotkey('a', lambda: input_set('a'))
    keyboard.add_hotkey('d', lambda: input_set('d'))
    keyboard.add_hotkey('s', lambda: input_set('s'))
    keyboard.add_hotkey('e', lambda: input_set('e'))
    keyboard.add_hotkey('q', lambda: input_set('q'))
    keyboard.add_hotkey('w', lambda: input_set('w'))
    keyboard.add_hotkey('space', lambda: input_set('space'))
    input_kased = {'a': lambda: tetris.liigu_tetromino("L"),
                      'd': lambda: tetris.liigu_tetromino("R"),
                      's': lambda: tetris.liigu_tetromino("D"),
                      'e': lambda: tetris.poora_tetromino(1),
                      'q': lambda: tetris.poora_tetromino(3),
                      'w': lambda: tetris.lange_tetromino()}

    input_set("")
    while True:  # Main loop
        # Mängu algus / lähtestamine
        if tetris.olek == 0 and jarg_input == "space":
            loo_tetris()

        # Kui mäng töötab
        if tetris.olek == 1:
            # Mängu loogika
            if jarg_input in ['w', 'a', 's', 'd', 'q', 'e']:
                input_kased[jarg_input]()
                jarg_input = ""
                tetris.kuva_tetromino()
                tetris.render()
                tetris.kuva_tetromino(True)
            if tetris.on_jargmine_tick:
                if not tetris.liigu_tetromino('D'):
                    tetris.kuva_tetromino()
                    tetris.kontrolli_rida()
                    tetris.otsusta_jargmine_tetromino()
                    if tetris.kontrolli_kokkuporget(tetris.tetromino_positsioon, tetris.praegune_tetromino):
                        tetris.naita_skoor()
                        tetris.peata()
                tetris.kuva_tetromino()
                tetris.render()
                tetris.kuva_tetromino(True)
            tetris.uuenda_taimer(0.5)

        # Mängust väljuda
        if tetris.olek == -1:
            break

        tahvel.update()
    raam.mainloop()
