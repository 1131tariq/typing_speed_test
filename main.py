from tkinter import *
from tkinter.simpledialog import askstring
import pyautogui
import pandas as pd
import random
import csv

# Data & Variables------------------------------------------------------------------------------------------------------

data = pd.read_csv("1000 most used english words.csv")
CPM = 0
WPM = 0
T = 60
WORDS = data["words"].tolist()
COMPLETED_WORDS = []
displayed_words = []
rw = 0
col = 0
position = 0
row = 0
timer_on = False

# Functionality---------------------------------------------------------------------------------------------------------
def add_score():
    rww = 1
    dat = pd.read_csv("scores.csv")
    SCOREBOARD_Names = dat["name"].tolist()
    SCOREBOARD_CPM = dat["CPM"].tolist()
    SCOREVOARD_WPM = dat["WPM"].tolist()
    x = len(SCOREBOARD_Names)-1
    try:
        score_entry = Label(scoreboard,
                            text=f"{SCOREBOARD_Names[x]} | CPM: {SCOREBOARD_CPM[x]} | WPM: {SCOREVOARD_WPM[x]}")
        score_entry.grid(row=rww, column=0)
    except:
        pass

def highlight():
    global position
    for x in range(0, position):
        display.winfo_children()[x].config(bg="#BAD7E9", fg="#000075", font=("sans", 10, "bold"))
    display.winfo_children()[position].config(bg="#90EE90")

def update():
    global displayed_words, col, rw
    col = 0
    rw = 0
    for widgets in display.winfo_children():
        widgets.destroy()
    for x in range(0, 18):
        randy = random.randint(0, len(WORDS) - 1)
        displayed_words.append(WORDS[randy])
        word = Label(display, text=displayed_words[x], bg="#BAD7E9", font=("sans", 10, "italic"), padx=5, pady=10,
                     justify="center", anchor="center")
        word.grid(column=col, row=rw)
        if col < 5:
            col += 1
        elif col > 4:
            col = 0
            rw += 1

def populate():
    global rw, col, displayed_words
    for x in range(0, 18):
        randy = random.randint(0, len(WORDS) - 1)
        displayed_words.append(WORDS[randy])
        word = Label(display, text=displayed_words[x], bg="#BAD7E9", font=("sans", 10, "italic"), pady=10)
        word.grid(column=col, row=rw)
        if col < 5:
            col += 1
        elif col > 4:
            col = 0
            rw += 1


def start_timer(self):
    global timer_on
    if not timer_on:
        countdown()

def countdown():
    global T, timer_on
    timer_on = True
    T -= 1
    if T >= 0:
        time.config(text=f"Time Remaining: {T} Secs")
        window.after(1000, countdown)
    else:
        user_input.config(state="disabled")
        name = askstring(title="Scoreboard Entry", prompt=f"Times up!\nYour CPM IS {CPM} and your WPM is {WPM}\nPlease enter your name:")
        dta = [name, CPM, WPM]
        with open("scores.csv", "a") as scores:
            writer = csv.writer(scores)
            writer.writerow(dta)
            add_score()



def temp_text(event):
    if user_input.get() == "Enter Test Here":
        user_input.delete(0, "end")


def next_word(event):
    global displayed_words, position, row, WORDS, COMPLETED_WORDS, WPM, CPM
    current_word = displayed_words[position]
    if user_input.get().lower() == current_word.lower() and T > 0:
        user_input.delete(0, END)
        pyautogui.press("backspace")
        COMPLETED_WORDS.append(current_word)
        WORDS.remove(current_word)
        position += 1
        if position == 18:
            displayed_words = []
            position = 0
            update()
        highlight()
        WPM = len(COMPLETED_WORDS)
        numbers = []
        for word in COMPLETED_WORDS:
            numbers.append(len(word))
        CPM = sum(numbers)
        cpm.config(text=f"CPM {CPM}")
        wpm.config(text=f"WPM {WPM}")

# GUI-------------------------------------------------------------------------------------------------------------------

window = Tk()
window.title("Typing Speed Test")
window.geometry("700x400")
window.config(bg="#2B3467")

Label(text="Typing Speed Test", bg="#2B3467", fg="white", font=("sans", 20, "bold")).grid(column=1, row=0)
Label(padx=20, justify="center", anchor="center",
      text="How fast are your fingers? Do the one-minute typing test to find out!\nPress the space bar after each word. At the end, you'll get your typing speed in CPM and WPM. Good luck!",
      bg="#2B3467", fg="white", font=("sans", 8)).grid(column=0, row=1, rowspan=2, columnspan=3)

test = Frame(window, bg="#2B3467", padx=20, pady=5)
test.grid(row=3, column=0, columnspan=3)

cpm = Label(test, width=27, text=f"CPM {CPM}", bg="#2B3467", fg="white")
cpm.grid(row=0, column=0)
wpm = Label(test, width=27, text=f"WPM {WPM}", bg="#2B3467", fg="white")
wpm.grid(row=0, column=1)
time = Label(test, width=27, text=f"Time remaining {T} secs", bg="#2B3467", fg="white")
time.grid(row=0, column=2)

display = Frame(test, bg="#BAD7E9", width=100)
display.grid(row=1, column=0, columnspan=3, rowspan=4)

user_input = Entry(test, justify="center")
user_input.insert(0, "Enter Test Here")
user_input.grid(row=5, column=0, columnspan=3)

scoreboard = Frame(pady=10, padx=10)
scoreboard.grid(row=6, column=0, columnspan=3)
Label(scoreboard, text="Most Recent Score").grid(row=0, column=0)

user_input.bind("<FocusIn>", temp_text)
user_input.bind("<space>", next_word)
user_input.bind("<KeyPress>", start_timer)

populate()
highlight()
add_score()

window.mainloop()
