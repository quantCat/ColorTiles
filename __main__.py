#!/usr/bin/env python3

from tkinter import *
import random

game = Tk()
WIDTH_FIELD = 500
HEIGHT_FIELD = 500
BUTTON_WIDTH = 10
BUTTON_HEIGHT = 1
DESK_SIZE = 8
cell_size = int(WIDTH_FIELD / DESK_SIZE)


def tiles_swapping(event):
    #print ("Click!", event.x, event.y)
    event.x -= event.x % cell_size
    event.y -= event.y % cell_size
    #print(event.widget.find_closest(event.x, event.y))
    field.itemconfig(CURRENT, fill = "#FFFFFF")


newgamebutton = Button(game, width = BUTTON_WIDTH, height = BUTTON_HEIGHT, text = "new game")
savebutton = Button(game, width = BUTTON_WIDTH, height = BUTTON_HEIGHT, text = "save game")
exitbutton = Button(game, width = BUTTON_WIDTH, height = BUTTON_HEIGHT, text = "exit game")
field = Canvas (game, width = WIDTH_FIELD, height = HEIGHT_FIELD)
field.tag_bind("cell", "<Button-1>", tiles_swapping)
#print(cell_size)

for i in range (DESK_SIZE):
    for j in range (DESK_SIZE):
        color = i+j
        if color >= 10:
            color = ord('a') + color - 9
        else:
            color = ord('0') + color
        color = "#" + chr(color) * 6
        #print(color)
        field.create_rectangle(i*cell_size, \
                               j*cell_size, \
                               (i+1)*cell_size, \
                                    (j+1)*cell_size, fill = color, tags = ("cell", color))


newgamebutton.grid(row=0)
savebutton.grid(row=0, column=1)
exitbutton.grid(row=0, column=2)
field.grid(row=1, columnspan=3)
game.mainloop()