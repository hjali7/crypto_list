import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io
import urllib.request
import crypto_data
import time
from search_module import SearchModule
from theme_module import ThemeModule

class CryptoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("لیست 100 ارز دیجیتال")
        self.root.geometry("400x600")
        self.images = []
        if not crypto_data.get_crypto_data():
            crypto_data.fetch_and_store_data()
        self.create_widgets()

    def load_image(self, url, size=(30, 30)):
        try:
            with urllib.request.urlopen(url) as u:
                raw_data = u.read()
            image = Image.open(io.BytesIO(raw_data))
            image = image.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        except:
            return None

    def create_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(fill="x", pady=5)

        self.title_label = ttk.Label(self.top_frame, text="لیست 100 ارز دیجیتال", font=("Arial", 14, "bold"))
        self.title_label.pack(side="left", padx=5)

        self.search_module = SearchModule(self.top_frame, self.update_list)
        self.theme_module = ThemeModule(self.top_frame, self.apply_theme)

        self.service_var = tk.StringVar(value=crypto_data.get_current_service())
        self.service_dropdown = ttk.OptionMenu(
            self.top_frame,
            self.service_var,
            crypto_data.get_current_service(),
            "coingecko",
            "coinmarketcap",
            command=self.switch_service
        )
        self.service_dropdown.pack(side="right", padx=5)

        self.refresh_button = ttk.Button(self.top_frame, text="Refresh", command=self.start_refresh)
        self.refresh_button.pack(side="right", padx=5)

        self.frame = ttk.Frame(self.root, style="Custom.TFrame")
        self.frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.frame)
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style="Custom.TFrame")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.update_list()

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.apply_theme()

    def apply_theme(self):
        theme = self.theme_module.get_theme()
        self.theme_module.configure_styles()

        self.root.configure(bg=theme["bg"])
        self.top_frame.configure(bg=theme["bg"])
        self.canvas.configure(bg=theme["bg"])

        self.title_label.configure(style="Custom.TLabel")
        self.service_dropdown.configure(style="Custom.TButton")
        self.refresh_button.configure(style="Custom.TButton")

    def update_list(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.images = []

        data = crypto_data.get_crypto_data()
        if not data:
            error_label = ttk.Label(self.scrollable_frame, text="خطا در دریافت داده‌ها", font=("Arial", 12), style="Custom.TLabel")
            error_label.pack(pady=10)
            return

        search_query = self.search_module.get_search_query()
        filtered_data = [item for item in data if search_query in item.get('name', '').lower()] if search_query else data

        for i, crypto in enumerate(filtered_data):
            row_frame = ttk.Frame(self.scrollable_frame, style="Custom.TFrame")
            row_frame.pack(fill="x", pady=2)

            image_url = crypto.get('image', '')
            photo = self.load_image(image_url)
            if photo:
                self.images.append(photo)
                logo_label = ttk.Label(row_frame, image=photo, style="Custom.TLabel")
                logo_label.pack(side="left", padx=5)

            name = crypto.get('name', 'N/A')
            price = crypto.get('current_price', 'N/A')
            label_text = f"{name}: ${price:.2f}"
            label = ttk.Label(row_frame, text=label_text, font=("Arial", 12), style="Custom.TLabel")
            label.pack(side="left")

    def switch_service(self, *args):
        selected_service = self.service_var.get()
        if crypto_data.fetch_and_store_data(selected_service):
            self.update_list()
        else:
            error_label = ttk.Label(self.scrollable_frame, text="خطا در تغییر سرویس", font=("Arial", 12), style="Custom.TLabel")
            error_label.pack(pady=10)

    def start_refresh(self):
        self.loading_label = ttk.Label(self.root, text="در حال به‌روزرسانی...", font=("Arial", 14), style="Custom.TLabel")
        self.loading_label.place(relx=0.5, rely=0.5, anchor="center")

        self.refresh_button.config(state="disabled")
        self.root.after(100, self.refresh_data_async)

    def refresh_data_async(self):
        time.sleep(1)

        if crypto_data.fetch_and_store_data(crypto_data.get_current_service()):
            self.update_list()
        else:
            error_label = ttk.Label(self.scrollable_frame, text="خطا در به‌روزرسانی داده‌ها", font=("Arial", 12), style="Custom.TLabel")
            error_label.pack(pady=10)

        self.loading_label.destroy()
        self.refresh_button.config(state="normal")

    def on_closing(self):
        crypto_data.close_db()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = CryptoListApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()