import tkinter as tk
from tkinter import ttk

class DetailsModule:
    def __init__(self, parent, crypto_data):
        self.parent = parent
        self.crypto_data = crypto_data
        self.show_details()

    def show_details(self):
        # پنجره جدید برای جزئیات
        self.details_window = tk.Toplevel(self.parent)
        self.details_window.title(f"جزئیات {self.crypto_data.get('name', 'N/A')}")
        self.details_window.geometry("400x300")

        # فریم اصلی
        frame = ttk.Frame(self.details_window)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # نام ارز
        name_label = ttk.Label(frame, text=f"نام: {self.crypto_data.get('name', 'N/A')}", font=("Arial", 14, "bold"))
        name_label.pack(anchor="w", pady=5)

        # قیمت فعلی
        price = self.crypto_data.get('current_price', 'N/A')
        price_label = ttk.Label(frame, text=f"قیمت فعلی: ${price:.2f}", font=("Arial", 12))
        price_label.pack(anchor="w", pady=5)

        # تغییرات 24 ساعته
        change_24h = self.crypto_data.get('price_change_percentage_24h', 'N/A')
        change_label = ttk.Label(frame, text=f"تغییرات 24 ساعته: {change_24h:.2f}%", font=("Arial", 12))
        change_label.pack(anchor="w", pady=5)

        # حجم معاملات
        volume = self.crypto_data.get('total_volume', 'N/A')
        volume_label = ttk.Label(frame, text=f"حجم معاملات 24 ساعته: ${volume:,.2f}", font=("Arial", 12))
        volume_label.pack(anchor="w", pady=5)

        # دکمه بستن
        close_button = ttk.Button(frame, text="بستن", command=self.details_window.destroy)
        close_button.pack(pady=10)

    def apply_theme(self, theme):
        # اعمال تم به پنجره جزئیات
        self.details_window.configure(bg=theme["bg"])
        for widget in self.details_window.winfo_children():
            if isinstance(widget, ttk.Frame):
                widget.configure(style="Custom.TFrame")
            for child in widget.winfo_children():
                if isinstance(child, ttk.Label):
                    child.configure(style="Custom.TLabel")
                elif isinstance(child, ttk.Button):
                    child.configure(style="Custom.TButton")