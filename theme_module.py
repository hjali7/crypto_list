import tkinter as tk
from tkinter import ttk

class ThemeModule:
    def __init__(self, parent, apply_theme_callback):
        self.parent = parent
        self.apply_theme_callback = apply_theme_callback  # برای فراخوانی apply_theme
        self.is_dark_mode = True  # حالت پیش‌فرض تیره
        self.themes = {
            "dark": {
                "bg": "#1C2526",
                "fg": "white",
                "button_bg": "#323739",
                "button_fg": "white",
                "button_active": "#424749",
                "op_color": "#00AEEF",
                "op_active": "#00CFFF",
                "special_bg": "#2A2F31",
                "special_fg": "#A0A0A0",
                "special_active": "#3A3F41"
            },
            "light": {
                "bg": "#F0F0F0",
                "fg": "black",
                "button_bg": "#D5D8DB",
                "button_fg": "black",
                "button_active": "#E0E0E0",
                "op_color": "#5B9BD5",
                "op_active": "#73AED6",
                "special_bg": "#B0B0B0",
                "special_fg": "#404040",
                "special_active": "#C0C0C0"
            }
        }
        self.setup_ui()

    def setup_ui(self):
        # دکمه تغییر تم
        self.theme_button = ttk.Button(
            self.parent,
            text="تغییر تم",
            command=self.toggle_theme
        )
        self.theme_button.pack(side="left", padx=5)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme_callback()

    def get_theme(self):
        return self.themes["dark" if self.is_dark_mode else "light"]

    def configure_button(self, button, text):
        theme = self.get_theme()
        if text in ['+', '-', '*', '/', '=']:
            button.config(
                style="Op.TButton",
                background=theme["op_color"],
                foreground="white",
                activebackground=theme["op_active"]
            )
        elif text in ['A', 'B', 'C', 'D', 'E', 'F', '<<', '>>', '(', ')', '%', '±']:
            button.config(
                style="Special.TButton",
                background=theme["special_bg"],
                foreground=theme["special_fg"],
                activebackground=theme["special_active"]
            )
        else:
            button.config(
                style="Normal.TButton",
                background=theme["button_bg"],
                foreground=theme["button_fg"],
                activebackground=theme["button_active"]
            )