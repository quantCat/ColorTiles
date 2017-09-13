#!/usr/bin/env python3

from tkinter import *
from random import *

game = Tk()
WIDTH_FIELD = 500
HEIGHT_FIELD = 500
BUTTON_WIDTH = 10
BUTTON_HEIGHT = 1
DESK_SIZE = 8
CELL_SIZE = int(WIDTH_FIELD / DESK_SIZE)
chosen_tile = 0
chosen_tile_color = 0
colors = []
colors_in_right_order = []


def desk_generation():
    global colors, colors_in_right_order
    for i in range(DESK_SIZE):
        for j in range(DESK_SIZE):
            color = i + j
            if color >= 10:
                color = ord('a') + color - 10
            else:
                color = ord('0') + color
            color = "#" + chr(color) * 6
            colors_in_right_order.append(color);
    colors = list(colors_in_right_order)
    shuffle(colors)


def tiles_swapping(event):
    global chosen_tile, chosen_tile_color
    event.x -= event.x % CELL_SIZE
    event.y -= event.y % CELL_SIZE
    if chosen_tile == 0:
        chosen_tile = field.find_closest(event.x, event.y)
        chosen_tile_color = field.itemcget(CURRENT, "fill")
    else:
        field.itemconfig(chosen_tile, fill=field.itemcget(CURRENT, "fill"))
        field.itemconfig(CURRENT, fill = chosen_tile_color)
        chosen_tile, chosen_tile_color = 0, 0


newgamebutton = Button(game, width = BUTTON_WIDTH, height = BUTTON_HEIGHT, text = "new game")
savebutton = Button(game, width = BUTTON_WIDTH, height = BUTTON_HEIGHT, text = "save game")
exitbutton = Button(game, width = BUTTON_WIDTH, height = BUTTON_HEIGHT, text = "exit game")
field = Canvas (game, width = WIDTH_FIELD, height = HEIGHT_FIELD)
field.tag_bind("cell", "<Button-1>", tiles_swapping)
#print(cell_size)


desk_generation()
print (colors)
print (colors_in_right_order)
for i in range (DESK_SIZE):
    #print("---")
    for j in range (DESK_SIZE):
        color = colors[i*DESK_SIZE + j]
        #print(i, j, color)
        right_color = colors_in_right_order[i*DESK_SIZE + j]
        field.create_rectangle(i * CELL_SIZE, \
                               j * CELL_SIZE, \
                               (i+1) * CELL_SIZE, \
                               (j+1) * CELL_SIZE, fill = color, tags = ("cell", right_color))


newgamebutton.grid(row=0)
savebutton.grid(row=0, column=1)
exitbutton.grid(row=0, column=2)
field.grid(row=1, columnspan=3)
game.mainloop()