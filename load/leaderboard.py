import tkinter as tk
from tkinter import ttk
import os

leaderboard_window_open = False  # Biến toàn cục để kiểm tra cửa sổ đã mở hay chưa

class Leaderboard:
    def __init__(self, master):
        self.master = master
        self.master.title("Leaderboard")

        self.tree = ttk.Treeview(master, columns=('Rank', 'Name', 'Money'), show='headings')
        self.tree.heading('Rank', text='Rank')
        self.tree.heading('Name', text='Player Name')
        self.tree.heading('Money', text='Money')

        # Đặt chiều rộng cho các cột
        self.tree.column('Rank', anchor='center', width=50)
        self.tree.column('Name', anchor='center', width=150)
        self.tree.column('Money', anchor='center', width=100)

        # Đặt màu nền
        self.tree.tag_configure('oddrow', background='lightblue')
        self.tree.tag_configure('evenrow', background='lightgreen')

        self.load_data()
        self.tree.pack(expand=True, fill='both')

    def load_data(self):
        load_path = os.path.join('load', 'load.txt')
        player_data = []
        try:
            with open(load_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.strip().split(' ', 1)
                    if len(parts) == 2:
                        name, money = parts
                        player_data.append((name, int(money)))
        except FileNotFoundError:
            print(f"File not found: {load_path}")
            return

        # Sắp xếp dữ liệu dựa trên số tiền
        sorted_data = sorted(player_data, key=lambda x: x[1], reverse=True)

        # Thêm dữ liệu vào treeview với rank
        for index, (name, money) in enumerate(sorted_data, start=1):
            if index % 2 == 0:
                self.tree.insert('', tk.END, values=(index, name, money), tags=('evenrow',))
            else:
                self.tree.insert('', tk.END, values=(index, name, money), tags=('oddrow',))

def show_leaderboard():
    global leaderboard_window_open
    if not leaderboard_window_open:
        leaderboard_window_open = True
        root = tk.Tk()
        app = Leaderboard(root)
        # Đặt xử lý khi cửa sổ đóng để reset trạng thái biến
        root.protocol("WM_DELETE_WINDOW", lambda: on_leaderboard_window_close(root))
        root.mainloop()

def on_leaderboard_window_close(window):
    global leaderboard_window_open
    leaderboard_window_open = False
    window.destroy()

