import tkinter as tk
from tkinter import ttk

class ThemeModule:
    def __init__(self, parent, apply_theme_callback):
        self.parent = parent
        self.apply_theme_callback = apply_theme_callback
        self.is_dark_mode = True
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
        self.style = ttk.Style()
        self.setup_ui()
        print("ThemeModule initialized with configure_styles and test_module methods")

    def setup_ui(self):
        self.theme_button = ttk.Button(
            self.parent,
            text="تغییر تم",
            command=self.toggle_theme
        )
        self.theme_button.pack(side="left", padx=5)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        print(f"Switching to {'dark' if self.is_dark_mode else 'light'} theme")
        self.apply_theme_callback()

    def get_theme(self):
        return self.themes["dark" if self.is_dark_mode else "light"]

    def configure_styles(self):
        theme = self.get_theme()
        self.style.configure("Custom.TFrame", background=theme["bg"])
        self.style.configure("Custom.TLabel", background=theme["bg"], foreground=theme["fg"])
        self.style.configure("Custom.TButton", background=theme["button_bg"], foreground=theme["button_fg"])
        print("Styles configured for theme")

    def test_module(self):
        print("ThemeModule is correctly loaded with version including test_module")