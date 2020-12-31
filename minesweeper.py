from collections import deque
import tkinter as tk
import random

# field setup
columns = 16
rows = 16
cell_x = 26
cell_y = 28
cell_qty = (columns * rows)
mine_qty = cell_qty // 5
empty_cell_qty = cell_qty - mine_qty

sequence = ['X'] * mine_qty + [0] * empty_cell_qty
random.shuffle(sequence)
mathfield = [sequence[columns * i:columns * (i + 1)] for i in range(rows)]
used = set()  # set for storing col and row for correct found fields


# filling mathfield with correct numbers
def fill_mathfield(row, col):
    global rows, columns, mathfield
    if mathfield[row][col] == 'X':
        return 'X'
    number = 0
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if 0 <= i < rows and 0 <= j < columns and mathfield[i][j] == 'X':
                number += 1
    return number


for row in range(rows):
    for col in range(columns):
        mathfield[row][col] = fill_mathfield(row, col)

# for i in mathfield:
#     print(i)


# defining interface
app = tk.Tk()
app.title("Minesweeper")
app.geometry(f"{columns * cell_x}x{rows * cell_y}+400+400")
app.resizable(False, False)
pic_flag = tk.PhotoImage(file='flag_icon.png')


def message_lost():
    """Show lose message"""
    reveal_field()
    message = tk.Label(
        background='red',
        font='helvetica 12',
        text='YOU LOST!'
    )
    message.grid(row=0, rowspan=rows, column=0, columnspan=columns)


def message_win():
    """Show win message"""
    reveal_field()
    message = tk.Label(
        background='green',
        font='helvetica 12',
        text='YOU WON!'
    )
    message.grid(row=0, rowspan=rows, column=0, columnspan=columns)


def visual_cell_open(r, c):
    """Visually update chosen cell and add it to [used] list"""
    used.add((r, c))
    minefield[r][c]['state'] = 'disabled'
    minefield[r][c]['background'] = 'lightgrey'
    if mathfield[r][c] == 0:
        minefield[r][c]['relief'] = 'flat'
        minefield[r][c]['text'] = ''
    elif mathfield[r][c] == 'X':
        minefield[r][c]['relief'] = 'raise'
        minefield[r][c]['text'] = mathfield[r][c]
        minefield[r][c]['disabledforeground'] = 'red'
    else:
        minefield[r][c]['relief'] = 'flat'
        minefield[r][c]['text'] = mathfield[r][c]


def reveal_field():
    """Reveal all cells after endgame"""
    global rows, columns
    for r in range(rows):
        for c in range(columns):
            visual_cell_open(r, c)


def check_solved():
    """Check if board is solved by counting 'disabled' cells on the board"""
    global rows, columns
    opened = 0
    for r in range(rows):
        for c in range(columns):
            if minefield[r][c]['state'] == 'disabled':
                opened += 1
    if opened == empty_cell_qty:
        message_win()


def open_zero_chain(r, c):
    """Open all 0 cells. Pretty similar to breadth first search"""
    global rows, columns
    q = deque([(r, c)])
    while q:
        r, c = q.popleft()
        used.add((r, c))
        for i in range(r - 1, r + 2):
            for j in range(c - 1, c + 2):
                if 0 <= i < rows and 0 <= j < columns:
                    if mathfield[i][j] == 0 and (i, j) not in used and (i, j) not in q:
                        q.append((i, j))
                    visual_cell_open(i, j)


def cell_r_click(event):
    """Handle Rclick event"""
    w = event.widget
    if w['state'] == 'normal':
        if w['image']:
            w['image'] = ''
        else:
            w['image'] = pic_flag


def cell_click(event):
    """Handle Lclick event"""
    global rows, columns
    w = event.widget
    if w['state'] == 'disabled' or w['image']:
        return
    r = w.grid_info()['row']
    c = w.grid_info()['column']
    if mathfield[r][c] == 'X':
        message_lost()
    elif mathfield[r][c] == 0:
        open_zero_chain(r, c)
    else:
        visual_cell_open(r, c)
    check_solved()


def bttn():
    """Define default button"""
    return tk.Button(
        width=2,
        height=1,
        borderwidth=3,
        font='helvetica 9',
        disabledforeground="black",
        background='linen',
        activebackground='linen',
        state='normal',
    )


# placing button widgets
minefield = [[0] * columns for z in range(rows)]

for row in range(rows):
    for col in range(columns):
        minefield[row][col] = bttn()
        minefield[row][col].bind('<Button-1>', cell_click)
        minefield[row][col].bind('<Button-3>', cell_r_click)
        minefield[row][col].grid(row=row, column=col)

# loop app
app.mainloop()
