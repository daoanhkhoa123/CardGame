from RPS.RPS_GUI import *
from load.load import load_player
from load.leaderboard import show_leaderboard
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Button  # Assuming macOS, if not, you can use tk.Button
from os import path
import os

_ASSET_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
background = os.path.join(_ASSET_DIRECTORY, "Asset_cards")
# Dimensions for the window
HEIGHT = 500
WIDTH = 1250

# Initialize the root Tkinter object
root = tk.Tk()
root.title("BlackJack Game")
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

def load_home():
    # Main frame with background image
    frame = tk.Frame(root, bg="green")
    frame.place(relwidth=1, relheight=1)

    # Load and place the background image
    image = Image.open(path.join(background, f"BlackJackMain.jpg"))
    render = ImageTk.PhotoImage(image)
    img = tk.Label(frame, image=render, bg='green')
    img.image = render
    img.place(relx=0, rely=0.01, relheight=0.987, relwidth=0.726)

    # BlackJack Label
    tk.Label(frame, text="BlackJack", fg='#811111', bg='green', font=('times', 37, 'bold')).place(relx=.79, rely=.12)
    
    # Button placement adjustments
    button_width = 200
    button_height = 50
    button_start_y = 0.25
    button_gap = 0.1

    # Play Button
    play_button = Button(frame, text="Play", fg='white', bg='blue', command=lambda: playgame(frame))
    play_button.place(relx=.8, rely=button_start_y, width=button_width, height=button_height)

    # Tutorial Button
    tutorial_button = Button(frame, text="Tutorial", fg='white', bg='blue', command=lambda: tutorial(frame))
    tutorial_button.place(relx=.8, rely=button_start_y + button_gap, width=button_width, height=button_height)

    # Leaderboard Button
    leaderboard_button = Button(frame, text="Leaderboard", fg='white', bg='blue', command=lambda: show_leaderboard())
    leaderboard_button.place(relx=.8, rely=button_start_y + 2*button_gap, width=button_width, height=button_height)

    #load button
    load_button = Button(frame, text="Load", fg='white', bg='blue', command=lambda: load_player(frame, root, load_button))
    load_button.place(relx=.8, rely=button_start_y + 3*button_gap, width=button_width, height=button_height)
    
    # Exit Button
    exit_button = Button(frame, text="Exit", fg='white', bg='blue', command=root.quit)
    exit_button.place(relx=.8, rely=button_start_y + 4*button_gap, width=button_width, height=button_height)


def playgame(frame):
    print("playgame - Implement the gameplay here.")
    
def tutorial(frame):
    pass

def leaderboard():
    show_leaderboard()


if __name__ == '__main__':
    load_home()
    root.mainloop()
