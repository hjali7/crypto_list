import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io
import urllib.request
import crypto_data
import time
from search_module import SearchModule
from theme_module import ThemeModule  # وارد کردن ماژول تم

class CryptoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("لیست 100 ارز دیجیتال")
        self.root.geometry("400x600")
        self.images = []  # برای نگهداری تصاویر
        # بارگذاری اولیه داده‌ها
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
        # پاک کردن ویجت‌های قبلی (برای رفرش)
        for widget in self.root.winfo_children():
            widget.destroy()

        # فریم بالا برای عنوان، جستجو، تم، انتخاب سرویس و دکمه رفرش
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill="x", pady=5)

        # عنوان
        self.title_label = ttk.Label(top_frame, text="لیست 100 ارز دیجیتال", font=("Arial", 14, "bold"))
        self.title_label.pack(side="left", padx=5)

        # اضافه کردن ماژول جستجو
        self.search_module = SearchModule(top_frame, self.update_list)

        # اضافه کردن ماژول تم
        self.theme_module = ThemeModule(top_frame, self.apply_theme)

        # منوی کشویی برای انتخاب سرویس
        self.service_var = tk.StringVar(value=crypto_data.get_current_service())
        self.service_dropdown = ttk.OptionMenu(
            top_frame,
            self.service_var,
            crypto_data.get_current_service(),
            "coingecko",
            "coinmarketcap",
            command=self.switch_service
        )
        self.service_dropdown.pack(side="right", padx=5)

        # دکمه رفرش
        self.refresh_button = ttk.Button(top_frame, text="Refresh", command=self.start_refresh)
        self.refresh_button.pack(side="right", padx=5)

        # فریم برای لیست
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        # اسکرول‌بار
        self.canvas = tk.Canvas(self.frame)
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # نمایش اولیه داده‌ها
        self.update_list()

        # چیدمان اسکرول‌بار و کانواس
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # اعمال تم اولیه
        self.apply_theme()

    def apply_theme(self):
        theme = self.theme_module.get_theme()

        # اعمال تم به رابط گرافیکی
        self.root.configure(bg=theme["bg"])
        self.top_frame.configure(bg=theme["bg"])
        self.frame.configure(bg=theme["bg"])
        self.canvas.configure(bg=theme["bg"])
        self.scrollable_frame.configure(bg=theme["bg"])
        self.title_label.configure(background=theme["bg"], foreground=theme["fg"])
        self.service_dropdown.configure(background=theme["button_bg"], foreground=theme["button_fg"])
        self.refresh_button.configure(background=theme["button_bg"], foreground=theme["button_fg"])

        # به‌روزرسانی لیست برای اعمال تم به لیبل‌ها
        self.update_list()

    def update_list(self):
        # پاک کردن لیست قبلی
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.images = []  # پاک کردن تصاویر قبلی

        # دریافت داده‌ها از ماژول
        data = crypto_data.get_crypto_data()
        if not data:
            error_label = ttk.Label(self.scrollable_frame, text="خطا در دریافت داده‌ها", font=("Arial", 12))
            error_label.pack(pady=10)
            theme = self.theme_module.get_theme()
            error_label.configure(background=theme["bg"], foreground=theme["fg"])
            return

        # فیلتر کردن بر اساس جستجو
        search_query = self.search_module.get_search_query()
        filtered_data = [item for item in data if search_query in item.get('name', '').lower()] if search_query else data

        # نمایش لیست ارزها
        theme = self.theme_module.get_theme()
        for i, crypto in enumerate(filtered_data):
            row_frame = ttk.Frame(self.scrollable_frame)
            row_frame.pack(fill="x", pady=2)
            row_frame.configure(bg=theme["bg"])

            # لوگو
            image_url = crypto.get('image', '')
            photo = self.load_image(image_url)
            if photo:
                self.images.append(photo)  # نگه‌داری تصویر برای جلوگیری از گارباژ کالکشن
                logo_label = ttk.Label(row_frame, image=photo)
                logo_label.pack(side="left", padx=5)
                logo_label.configure(background=theme["bg"])

            # نام و قیمت
            name = crypto.get('name', 'N/A')
            price = crypto.get('current_price', 'N/A')
            label_text = f"{name}: ${price:.2f}"
            label = ttk.Label(row_frame, text=label_text, font=("Arial", 12))
            label.pack(side="left")
            label.configure(background=theme["bg"], foreground=theme["fg"])

    def switch_service(self, *args):
        # تغییر سرویس و رفرش داده‌ها
        selected_service = self.service_var.get()
        if crypto_data.fetch_and_store_data(selected_service):
            self.update_list()
        else:
            error_label = ttk.Label(self.scrollable_frame, text="خطا در تغییر سرویس", font=("Arial", 12))
            error_label.pack(pady=10)
            theme = self.theme_module.get_theme()
            error_label.configure(background=theme["bg"], foreground=theme["fg"])

    def start_refresh(self):
        # نمایش طرح به‌روزرسانی
        self.loading_label = ttk.Label(self.root, text="در حال به‌روزرسانی...", font=("Arial", 14))
        self.loading_label.place(relx=0.5, rely=0.5, anchor="center")
        theme = self.theme_module.get_theme()
        self.loading_label.configure(background=theme["bg"], foreground=theme["fg"])

        # غیرفعال کردن دکمه رفرش موقع لودینگ
        self.refresh_button.config(state="disabled")

        # به‌روزرسانی داده‌ها توی پس‌زمینه
        self.root.after(100, self.refresh_data_async)

    def refresh_data_async(self):
        # شبیه‌سازی تاخیر
        time.sleep(1)

        # به‌روزرسانی داده‌ها
        if crypto_data.fetch_and_store_data(crypto_data.get_current_service()):
            self.update_list()
        else:
            error_label = ttk.Label(self.scrollable_frame, text="خطا در به‌روزرسانی داده‌ها", font=("Arial", 12))
            error_label.pack(pady=10)
            theme = self.theme_module.get_theme()
            error_label.configure(background=theme["bg"], foreground=theme["fg"])

        # حذف طرح به‌روزرسانی و فعال کردن دکمه
        self.loading_label.destroy()
        self.refresh_button.config(state="normal")

    def on_closing(self):
        # بستن دیتابیس و خروج
        crypto_data.close_db()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = CryptoListApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()