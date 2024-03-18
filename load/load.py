import tkinter as tk
from tkinter import messagebox
import os

class LineByLineLoad:
    def __init__(self, master, load_button):
        self.master = master
        self.load_button = load_button  # Store the load_button reference
        self.selected_player = None
        self.apply_button = tk.Button(master, text="Apply", command=self.apply_selection)
        self.apply_button.pack(pady=20)

        self.master.title("Load Player")

        self.display_label = tk.Label(master, text="Select a player", wraplength=400)
        self.display_label.pack(pady=20)

        self.button_frame = tk.Frame(master)  # Frame to hold the buttons for each player
        self.button_frame.pack(pady=10)

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
                name,money = line.strip().split()  # Assuming each line has a player name
                player_button = tk.Button(self.button_frame, text=f"Player : {name} -  {money} $",  command=lambda n=name, m=money: self.display_player(n, m))
                player_button.pack(pady=2, padx=4, anchor='w')
        else:
            messagebox.showinfo("Error", "No players found.")
            self.master.destroy()

    def display_player(self, name,money):
        self.selected_player = (name, money)
        self.display_label.config(text=f"Selected Player: {name}")
        self.load_button.config(text=f"Load player:  {name}-{money} $")  # Update the Load button text

    def apply_selection(self):
        if self.selected_player:
            name, money = self.selected_player
            self.load_button.config(text=f"Load player: {name} - {money} $")
            self.master.destroy()  # Optional: Close the load window upon applying
        else:
            messagebox.showinfo("Error", "No player selected.")


def load_player(frame, root, load_button):
    load_window = tk.Toplevel(root)
    LineByLineLoad(load_window, load_button)

