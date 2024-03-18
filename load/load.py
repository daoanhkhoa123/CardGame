import tkinter as tk
from tkinter import messagebox, Button
import os

class LineByLineLoad:
    def __init__(self, master, load_button, apply_change):
        self.master = master
        self.load_button = load_button
        self.apply_change = apply_change
        self.selected_player = None
        self.master.title("Load Player")

        self.display_label = tk.Label(master, text="Select a player", wraplength=400)
        self.display_label.pack(pady=20)

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)

        self.apply_button = Button(master, text="Apply", command=self.apply_selection)
        self.apply_button.pack(pady=10)

        self.load_players()

    def load_players(self):
        load_path = os.path.join('load', 'load.txt')
        try:
            with open(load_path, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            messagebox.showinfo("Error", f"File not found: {load_path}")
            self.master.destroy()
            return

        if lines:
            for line in lines:
                name, money = line.strip().split()
                player_button = tk.Button(self.button_frame, text=f"Player: {name} - {money}$", 
                                          command=lambda n=name, m=money: self.select_player(n, m))
                player_button.pack(pady=2, padx=4, anchor='w')
        else:
            messagebox.showinfo("Error", "No players found.")
            self.master.destroy()

    def select_player(self, name, money):
        self.selected_player = (name, money)
        self.display_label.config(text=f"Selected Player: {name} - {money}$")

    def apply_selection(self):
        if self.selected_player:
            name, money = self.selected_player
            self.load_button.config(text=f"Load player: {name} - {money}$")
            self.apply_change(name, money)
            global load_window_open
            load_window_open = False  # Reset the flag when apply is clicked
            self.master.destroy()

def load_player(frame, root, load_button):
    global load_window_open
    if not load_window_open:
        load_window_open = True
        load_window = tk.Toplevel(root)
        load_window.protocol("WM_DELETE_WINDOW", lambda: on_load_window_close())
        LineByLineLoad(load_window, load_button, apply_change)

def apply_change(name, money):
    # Function to handle the selected player data
    pass

def on_load_window_close():
    global load_window_open
    load_window_open = False  # Reset the flag when the load window is closed manually

load_window_open = False  # Initialize the flag

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    load_button = tk.Button(root, text="Load Player", command=lambda: load_player(None, root, load_button))
    load_button.pack()
    root.mainloop()
