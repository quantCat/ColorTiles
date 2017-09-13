#!/usr/bin/env python3

from tkinter import *
from random import *

game = Tk()
WIDTH_FIELD = 800
HEIGHT_FIELD = 700
BUTTON_WIDTH = 10
BUTTON_HEIGHT = 1
DESK_WIDTH = 3
DESK_HEIGHT = 3
# Max size with current algorithm is 8x9
CELL_WIDTH = int(WIDTH_FIELD / DESK_WIDTH)
CELL_HEIGHT = int (HEIGHT_FIELD / DESK_HEIGHT)
HIGHLIGHT_COLOR = "blue"

chosen_tile = 0
chosen_tile_color = 0
colors = []
colors_in_right_order = []

# TODO:
# various desks generating


def desk_generation():
    global colors, colors_in_right_order
    for i in range(DESK_WIDTH):
        for j in range(DESK_HEIGHT):
            color = i + j
            if color >= 10:
                color = ord('a') + color - 10
            else:
                color = ord('0') + color
            color = "#" + chr(color) * 6
            colors_in_right_order.append(color);
            # print(color, end=' ')
        # print()
    colors = list(colors_in_right_order)
    shuffle(colors)


def checking_is_game_finished():
    for i in range (DESK_WIDTH):
        for j in range (DESK_HEIGHT):
            index = i*DESK_HEIGHT + j
            # print(field.find_withtag(index+1))
            # print (field.itemcget(field.find_withtag(index+1), "fill"))
            # print(colors_in_right_order[index])
            if field.itemcget(field.find_withtag(index+1), "fill") != colors_in_right_order[index]:
                return False
    return True


def tiles_swapping(event):
    global chosen_tile, chosen_tile_color
    event.x -= event.x % CELL_WIDTH
    event.y -= event.y % CELL_HEIGHT
    if chosen_tile == 0:
        chosen_tile = field.find_closest(event.x, event.y)
        chosen_tile_color = field.itemcget(CURRENT, "fill")
        # field.itemconfig(CURRENT, outline="red")
        highlight_coords = field.coords(CURRENT)
        field.create_rectangle(highlight_coords, fill="", outline=HIGHLIGHT_COLOR, tag="highlight")
    else:
        # field.itemconfig(chosen_tile, outline="black")
        field.delete("highlight")
        field.itemconfig(chosen_tile, fill=field.itemcget(CURRENT, "fill"))
        field.itemconfig(CURRENT, fill=chosen_tile_color)
        chosen_tile, chosen_tile_color = 0, 0
        game_is_finished = checking_is_game_finished()
        if game_is_finished:
            # field.destroy()
            # game_win_text = Label(game, text="A winner is you!")
            # game_win_text.grid(row=1, columnspan=3)
            field.create_text(WIDTH_FIELD/2, HEIGHT_FIELD/2, anchor="center", font=("Purisa", 40),\
                              text="A WINNER IS YOU!", fill=HIGHLIGHT_COLOR)
            field.config(state="disabled")


newgamebutton = Button(game, width = BUTTON_WIDTH, height = BUTTON_HEIGHT, text = "new game")
savebutton = Button(game, width = BUTTON_WIDTH, height = BUTTON_HEIGHT, text = "save game")
exitbutton = Button(game, width = BUTTON_WIDTH, height = BUTTON_HEIGHT, text = "exit game")
field = Canvas (game, width = WIDTH_FIELD, height = HEIGHT_FIELD)
field.tag_bind("cell", "<Button-1>", tiles_swapping)
# print(cell_size)


desk_generation()
for i in range (DESK_WIDTH):
    for j in range (DESK_HEIGHT):
        index = i*DESK_HEIGHT + j
        color = colors[index]
        right_color = colors_in_right_order[index]
        field.create_rectangle(i * CELL_WIDTH, \
                               j * CELL_HEIGHT, \
                               (i+1) * CELL_WIDTH, \
                               (j+1) * CELL_HEIGHT, fill = color, tags = ("cell", index+1, right_color))
        # print (index, color, end=' ')
    # print()


newgamebutton.grid(row=0)
savebutton.grid(row=0, column=1)
exitbutton.grid(row=0, column=2)
field.grid(row=1, columnspan=3)
game.mainloop()