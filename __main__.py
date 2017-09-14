#!/usr/bin/env python3

from tkinter import *
from random import *

game = Tk()
WIDTH_FIELD = 800
HEIGHT_FIELD = 700
BUTTON_WIDTH = 10
BUTTON_HEIGHT = 1
DESK_WIDTH = 5
DESK_HEIGHT = 5
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


def checking_is_game_finished():
    for i in range (DESK_WIDTH):
        for j in range (DESK_HEIGHT):
            index = i*DESK_HEIGHT + j
            if field.itemcget(field.find_withtag(index+1), "fill") != colors_in_right_order[index]:
                return False
    return True


def game_finishing():
    field.delete("color_mark")
    field.create_text(WIDTH_FIELD / 2, HEIGHT_FIELD / 2, anchor="center", font=("Purisa", 40), \
                      text="A WINNER IS YOU!", fill=HIGHLIGHT_COLOR)
    field.config(state="disabled")


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


def color_marks_coords (rectangle_coords):
    print (rectangle_coords)
    oval_rad1 = CELL_WIDTH//6
    oval_rad2 = CELL_HEIGHT//6
    x_center = (rectangle_coords[0] + rectangle_coords[2]) / 2.0
    y_center = (rectangle_coords[1] + rectangle_coords[3]) / 2.0  # arithmetic mean
    circle_coords = [x_center - oval_rad1, y_center - oval_rad2, x_center + oval_rad1, y_center + oval_rad2]
    return circle_coords


def desk_creating():
    for i in range(DESK_WIDTH):
        for j in range(DESK_HEIGHT):
            index = i * DESK_HEIGHT + j
            color = colors[index]
            right_color = colors_in_right_order[index]
            field.create_rectangle(i * CELL_WIDTH,
                                   j * CELL_HEIGHT,
                                   (i + 1) * CELL_WIDTH,
                                   (j + 1) * CELL_HEIGHT, fill=color, tags=("cell", index + 1, right_color))
            # print (index, color, end=' ')
            # print()
    field.create_oval(color_marks_coords(field.coords(1)),
                      fill=colors_in_right_order[0],
                      outline=HIGHLIGHT_COLOR, tag="color_mark")  # nw
    field.create_oval(color_marks_coords(field.coords(DESK_HEIGHT)),
                      fill=colors_in_right_order[DESK_HEIGHT-1],
                      outline=HIGHLIGHT_COLOR, tag="color_mark")  # sw
    field.create_oval(color_marks_coords(field.coords((DESK_HEIGHT * (DESK_WIDTH - 1) + 1))),
                      fill=colors_in_right_order[(DESK_HEIGHT * (DESK_WIDTH - 1))],
                      outline=HIGHLIGHT_COLOR, tag="color_mark")  # ne
    field.create_oval(color_marks_coords(field.coords(DESK_HEIGHT * DESK_WIDTH)),
                      fill=colors_in_right_order[DESK_HEIGHT * DESK_WIDTH - 1],
                      outline=HIGHLIGHT_COLOR, tag="color_mark")  # se


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
            game_finishing()


newgamebutton = Button(game, width = BUTTON_WIDTH, height = BUTTON_HEIGHT, text = "new game")
savebutton = Button(game, width = BUTTON_WIDTH, height = BUTTON_HEIGHT, text = "save game")
exitbutton = Button(game, width = BUTTON_WIDTH, height = BUTTON_HEIGHT, text = "exit game")
field = Canvas (game, width = WIDTH_FIELD, height = HEIGHT_FIELD)
field.tag_bind("cell", "<Button-1>", tiles_swapping)
# print(cell_size)


desk_generation()
desk_creating()


newgamebutton.grid(row=0)
savebutton.grid(row=0, column=1)
exitbutton.grid(row=0, column=2)
field.grid(row=1, columnspan=3)
game.mainloop()