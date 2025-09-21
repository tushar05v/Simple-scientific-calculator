from tkinter import *
import re
from calc_logic import evaluate_expression, clear, delete_last

# Initialize main window
app = Tk()
app.geometry("400x420+52+52")
app.config(background="gray11")
app.resizable(False, False)
app.overrideredirect(1)

def smooth_resize_height(target_height, steps=20, delay=10):
    current_geometry = app.winfo_geometry()
    size_part = current_geometry.split("+")[0]
    current_width, current_height = map(int, size_part.split("x"))

    height_diff = (target_height - current_height) / steps

    def step(i=1):
        if i > steps:
            return
        new_height = int(current_height + height_diff * i)
        app.geometry(f"{current_width}x{new_height}")
        app.after(delay, step, i + 1)

    step()

std = True

# Entry widget
entryVar = StringVar()
entry = Entry(
    app,
    textvariable=entryVar,
    background="gray20",
    border=0,
    foreground="white",
    font=("Helvetica", 27)
)
entry.grid(columnspan=4, ipady=15, pady=(5,5))

# Button labels
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+',
    'C', 'X', 'close', 'Sci',
    'sqrt', 'π', 'tan', 'cos',
    'log', 'sin','(', ')'
]

# Special function handlers
def eq():
    expression = entryVar.get()
    entryVar.set(evaluate_expression(expression))

def x():
    entryVar.set(delete_last(entryVar.get()))

def C():
    entryVar.set(clear())

def close():
    app.destroy()

def Sc():
    global std
    if std:
        smooth_resize_height(540)
        buttons_dict['Sci'].config(text="Std")
        std = False
    else:
        smooth_resize_height(420)
        buttons_dict['Sci'].config(text="Sci")
        std = True

# Mapping special buttons to their functions
special_functions = {
    '=': eq,
    'X': x,
    'C': C,
    'close': close,
    'Sci': Sc
}

# Button click handler
def on_button_click(value):
    text = entryVar.get()
    operators = '+-*/'

    # Prevent starting with operator
    if text == '' and value in operators:
        return

    # Handle special function buttons
    if value in special_functions:
        special_functions[value]()
        return

    # Prevent multiple decimals in the same number
    if value == '.':
        last_number = re.split(r'[+\-*/]', text)[-1]
        if '.' in last_number:
            return

    # Prevent consecutive operators or dots
    if text and text[-1] in operators + '.' and value in operators + '.':
        return

    # Append valid value to entry
    entryVar.set(text + value)


# Create and place buttons
buttons_dict = {}
row = 1
col = 0

for label in buttons:
    btn = Button(
        app,
        text=label,
        font=("Helvetica", 18),
        background="gray30",
        foreground="white",
        command=lambda val=label: on_button_click(val)
    )
    btn.grid(row=row, column=col, ipady=5, sticky=E+W)
    if label == "=":
        btn.config(background="darkorange1", foreground="white")
    elif label in ("C", "X"):
        btn.grid_configure(row=row, column=col, columnspan=2, ipady=5, sticky=E+W)
        col += 1
    elif label == "close":
        btn.config(bg="red", border=0)
        btn.grid_configure(row=row, column=col, columnspan=3, ipady=5, sticky=E+W)
        col += 2
    elif label == "Sci":
        btn.config(bg="gray11", border=0)

    buttons_dict[label] = btn

    col += 1
    if col > 3:
        col = 0
        row += 1

# Start the app
app.mainloop()
