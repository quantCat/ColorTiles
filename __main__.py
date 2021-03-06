#!/usr/bin/env python3

from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from random import *

game = Tk()
moves = 0
WIDTH_FIELD = 800
HEIGHT_FIELD = 700
BUTTON_WIDTH = 10
BUTTON_HEIGHT = 1
desk_width = 3
desk_height = 3
# Max size with current algorithm is 8x9
CELL_WIDTH = int(WIDTH_FIELD / desk_width)
CELL_HEIGHT = int(HEIGHT_FIELD / desk_height)
HIGHLIGHT_COLOR = "blue"


def generate_color():
    return [randint(0, 256-1), randint(0, 256-1), randint(0, 256-1)]


chosen_tile = 0
chosen_tile_color = 0
colors = []
colors_in_right_order = []
corner_colors = {}


def checking_is_game_finished():
    for i in range(desk_width):
        for j in range(desk_height):
            index = i * desk_height + j
            if field.itemcget(field.find_withtag(index+1), "fill") != colors_in_right_order[index]:
                return False
    return True


def game_finishing():
    global moves
    field.delete("color_mark")
    field.create_text(WIDTH_FIELD / 2, HEIGHT_FIELD / 2, anchor="center", font=("Purisa", 40), \
                      text="A WINNER IS YOU! \nMoves: {}".format(moves), fill=HIGHLIGHT_COLOR)
    field.config(state="disabled")


def desk_generation(_event):
    global colors, colors_in_right_order, desk_width, desk_height, corner_colors, CELL_HEIGHT, CELL_WIDTH
    desk_width = simpledialog.askinteger\
        ("Enter width", "Please enter the width of the desk in cells", minvalue=3, maxvalue=30)
    desk_height = simpledialog.askinteger\
        ("Enter height", "Please enter the height of the desk in cells", minvalue=3, maxvalue=30)
    CELL_WIDTH = int(WIDTH_FIELD / desk_width)
    CELL_HEIGHT = int(HEIGHT_FIELD / desk_height)
    field.delete("greeting")
    colors.clear()
    colors_in_right_order.clear()
    corner_colors = {'ul': generate_color(), 'ur': generate_color(), 'll': generate_color(), 'lr': generate_color()}
    for i in range(desk_height):

        color1r = (corner_colors['ul'][0] * (desk_height - 1 - i) + corner_colors['ll'][0] * i) // (desk_height - 1)
        color1g = (corner_colors['ul'][1] * (desk_height - 1 - i) + corner_colors['ll'][1] * i) // (desk_height - 1)
        color1b = (corner_colors['ul'][2] * (desk_height - 1 - i) + corner_colors['ll'][2] * i) // (desk_height - 1)

        color2r = (corner_colors['ur'][0] * (desk_height - 1 - i) + corner_colors['lr'][0] * i) // (desk_height - 1)
        color2g = (corner_colors['ur'][1] * (desk_height - 1 - i) + corner_colors['lr'][1] * i) // (desk_height - 1)
        color2b = (corner_colors['ur'][2] * (desk_height - 1 - i) + corner_colors['lr'][2] * i) // (desk_height - 1)

        for j in range(desk_width):
            colorr = (color1r * (desk_width - 1 - j) + color2r * j) // (desk_width - 1)
            colorg = (color1g * (desk_width - 1 - j) + color2g * j) // (desk_width - 1)
            colorb = (color1b * (desk_width - 1 - j) + color2b * j) // (desk_width - 1)
            print("color generation: ", colorr, colorg, colorb)
            colors_in_right_order.append('#{}'.format(bytes([colorr, colorg, colorb]).hex()))
    colors = list(colors_in_right_order)
    shuffle(colors)
    desk_creating()


def color_marks_coords(rectangle_coords):
    # print(rectangle_coords)
    oval_rad1 = CELL_WIDTH//6
    oval_rad2 = CELL_HEIGHT//6
    x_center = (rectangle_coords[0] + rectangle_coords[2]) / 2.0
    y_center = (rectangle_coords[1] + rectangle_coords[3]) / 2.0  # arithmetic mean
    circle_coords = [x_center - oval_rad1, y_center - oval_rad2, x_center + oval_rad1, y_center + oval_rad2]
    return circle_coords


def desk_creating():
    global desk_width, desk_height, moves
    moves = 0
    field.config(state="normal")
    for i in range(desk_width):
        for j in range(desk_height):
            index = i * desk_height + j
            color = colors[index]
            right_color = colors_in_right_order[index]
            field.create_rectangle(i * CELL_WIDTH,
                                   j * CELL_HEIGHT,
                                   (i + 1) * CELL_WIDTH,
                                   (j + 1) * CELL_HEIGHT, fill=color, tags=("cell", index + 1, right_color))
            print (index, color, end=' ')
            print()
    field.create_oval(color_marks_coords(field.coords(1)),
                      fill='#{}'.format(bytes(corner_colors['ul']).hex()),
                      outline=HIGHLIGHT_COLOR, tag="color_mark")  # nw
    field.create_oval(color_marks_coords(field.coords(desk_height)),
                      fill='#{}'.format(bytes(corner_colors['ur']).hex()),
                      outline=HIGHLIGHT_COLOR, tag="color_mark")  # sw
    field.create_oval(color_marks_coords(field.coords((desk_height * (desk_width - 1) + 1))),
                      fill='#{}'.format(bytes(corner_colors['ll']).hex()),
                      outline=HIGHLIGHT_COLOR, tag="color_mark")  # ne
    field.create_oval(color_marks_coords(field.coords(desk_height * desk_width)),
                      fill='#{}'.format(bytes(corner_colors['lr']).hex()),
                      outline=HIGHLIGHT_COLOR, tag="color_mark")  # se


def load_game(_event):
    global colors, colors_in_right_order
    try:
        with open("save.txt", "r") as f:
            colors_in_right_order = f.readline().strip().split(" ")
            colors = f.readline().strip().split(" ")
            desk_creating()
    except FileExistsError:
        print("No saved game")


def save_game(_event):
    text2save = " ".join(colors_in_right_order)+"\n"+" ".join(colors)
    print(text2save)
    with open("save.txt", "w") as f:
        f.write(text2save)


def quit_game(_event):
    if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        game.destroy()


def tiles_swapping(event):
    global chosen_tile, chosen_tile_color, moves
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
        if field.itemcget(CURRENT, "fill") != chosen_tile_color:
            moves += 1
            field.itemconfig(chosen_tile, fill=field.itemcget(CURRENT, "fill"))
            field.itemconfig(CURRENT, fill=chosen_tile_color)
        chosen_tile, chosen_tile_color = 0, 0
        game_is_finished = checking_is_game_finished()
        if game_is_finished:
            game_finishing()


newbutton = Button(game, width = BUTTON_WIDTH, height = BUTTON_HEIGHT, text ="new game")
loadbutton = Button(game, width = BUTTON_WIDTH, height = BUTTON_HEIGHT, text = "load game")
savebutton = Button(game, width = BUTTON_WIDTH, height = BUTTON_HEIGHT, text = "save game")
exitbutton = Button(game, width = BUTTON_WIDTH, height = BUTTON_HEIGHT, text = "exit game")
field = Canvas (game, width = WIDTH_FIELD, height = HEIGHT_FIELD)
field.tag_bind("cell", "<Button-1>", tiles_swapping)
newbutton.bind("<Button-1>", desk_generation)
loadbutton.bind("<Button-1>", load_game)
savebutton.bind("<Button-1>", save_game)
exitbutton.bind("<Button-1>", quit_game)
# print(cell_size)

newbutton.grid(row=0)
loadbutton.grid(row=0, column=1)
savebutton.grid(row=0, column=2)
exitbutton.grid(row=0, column=3)
field.grid(row=1, columnspan=4)
#field.create_text(WIDTH_FIELD / 2, HEIGHT_FIELD / 2, anchor="center", font=("Purisa", 20), \
 #                     text="Press 'New game'\n to start a new game", fill=HIGHLIGHT_COLOR, tag='greeting')

game.mainloop()
