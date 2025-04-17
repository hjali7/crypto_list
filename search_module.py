import tkinter as tk
from tkinter import ttk

class SearchModule:
    def __init__(self, parent, update_callback):
        self.parent = parent
        self.update_callback = update_callback  # برای فراخوانی update_list
        self.search_var = tk.StringVar()
        self.setup_ui()

    def setup_ui(self):
        # کادر جستجو
        self.search_entry = ttk.Entry(self.parent, textvariable=self.search_var)
        self.search_entry.pack(side="left", padx=5)
        search_button = ttk.Button(self.parent, text="جستجو", command=self.search_crypto)
        search_button.pack(side="left", padx=5)

    def search_crypto(self):
        # فراخوانی متد update_list برای به‌روزرسانی لیست
        self.update_callback()

    def get_search_query(self):
        return self.search_var.get().lower()