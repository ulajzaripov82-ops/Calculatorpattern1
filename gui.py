# gui.py
import tkinter as tk
from tkinter import ttk
from utils import load_button_img, resize_image
from logic import CalculatorLogic

class CalculatorApp:
    def __init__(self, root):
        self.root = root                     # ← ЭТО БЫЛО ПРОПУЩЕНО
        self.root.title("My first Calculator")
        self.root.geometry("360x540")
        self.root.resizable(True, True)
        self.root.configure(bg="white")

        # Константы кнопок
        self.buttons_list = [
            "MC", "MR", "M+", "M-",
            "C", "()", "<-", "+",
            "7", "8", "9", "-",
            "4", "5", "6", "/",
            "1", "2", "3", "*",
            "+/-", "0", ",", "=",
        ]

        # Загружаем оригиналы картинок (укажи свои пути)
        self.digit_img = load_button_img(r"C:\Users\admin\OneDrive\Desktop\calculator 1000 str\images for calculator\babymonster asa _ SBS GAYO DAEJEON SUMMER 2025 (270725) (1).png")
        self.operator_img = load_button_img(r"C:\Users\admin\OneDrive\Desktop\calculator 1000 str\images for calculator\загруженное (4) (1).png")
        self.memory_img = load_button_img(r"C:\Users\admin\OneDrive\Desktop\calculator 1000 str\images for calculator\☆Wonhee☆ (1).png")

        # Словари для хранения кнопок и текстур
        self.buttons_dict = {}
        self.textures_dict = {}

        # Создаём дисплей
        self.display = ttk.Entry(self.root, font=("Arial", 22), justify="right")
        self.display.grid(row=0, column=0, columnspan=4, sticky="we", padx=15, pady=30)

        # Создаём логику, передавая дисплей
        self.logic = CalculatorLogic(self.display)

        # Создаём кнопки
        self.create_buttons()

        # Настройка сетки, чтобы кнопки растягивались
        for i in range(1, 8):
            self.root.rowconfigure(i, weight=1)
        for i in range(4):
            self.root.columnconfigure(i, weight=1)

        # Переменные для защиты от частых ресайзов
        self.last_width = 360
        self.last_height = 540
        self.resize_scheduled = False

        # Привязка событий
        self.root.bind("<Configure>", self.on_configure)
        self.root.bind("<Key>", self.press_key)

        # Первичная отрисовка картинок
        self.root.update()
        self.resize_images()

    def create_buttons(self):
        row_idx = 1
        col_idx = 0

        for btn_text in self.buttons_list:
            btn = tk.Button(
                self.root,
                text=btn_text,
                compound="center",
                fg="white",
                font=("Arial", 16, "bold"),
                borderwidth=0,
                relief="flat",
                highlightthickness=0,
                activebackground=self.root.cget("bg"),
                command=lambda b=btn_text: self.logic.button_click(b, self.animate_button_press)
            )
            btn.grid(row=row_idx, column=col_idx, sticky="nsew", padx=(0, 1), pady=(0, 1))
            self.buttons_dict[btn_text] = btn

            # Переход к следующей колонке
            col_idx += 1
            # Перенос на новую строку, если колонок больше 3
            if col_idx > 3:
                col_idx = 0
                row_idx += 1


    def on_configure(self, event):
        # Игнорируем события не от корневого окна
        if event.widget != self.root:
            return
        # Защита от частых вызовов
        new_width = self.root.winfo_width()
        new_height = self.root.winfo_height()
        if new_width == self.last_width and new_height == self.last_height:
            return
        self.last_width = new_width
        self.last_height = new_height

        # Отложенный ресайз (не вызываем сразу, чтобы не тормозить)
        if not self.resize_scheduled:
            self.resize_scheduled = True
            self.root.after(100, self._delayed_resize)

    def _delayed_resize(self):
        self.resize_scheduled = False
        self.resize_images()

    def resize_images(self):
        # Получаем размеры окна
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        btn_width = max(50, (width - 3) // 4)
        btn_height = max(40, (height - 100 - 5) // 6)

        for btn_text, btn in self.buttons_dict.items():
            # Выбираем оригинал в зависимости от типа кнопки
            if btn_text in ("MC", "MR", "M+", "M-"):
                base = self.memory_img
            elif btn_text in ("+", "-", "*", "/", "=", "C", "<-", "()"):
                base = self.operator_img
            else:
                base = self.digit_img

            normal_tk = resize_image(base, btn_width, btn_height, brightness=1.0)
            dark_tk = resize_image(base, btn_width, btn_height, brightness=0.6)
            self.textures_dict[btn_text] = (normal_tk, dark_tk)
            btn.config(image=normal_tk)

    def animate_button_press(self, btn_text):
        if btn_text in self.textures_dict:
            btn = self.buttons_dict[btn_text]
            normal_tex, dark_tex = self.textures_dict[btn_text]
            btn.config(image=dark_tex)
            self.root.after(100, lambda: btn.config(image=normal_tex))

    def press_key(self, event):
        char = event.char
        keysym = event.keysym

        if char in "0123456789+-*/()":
            self.logic.button_click(char, self.animate_button_press)
        elif char in ",.":
            self.logic.button_click(",", self.animate_button_press)
        elif keysym == "Return":
            self.logic.button_click("=", self.animate_button_press)
        elif keysym == "BackSpace":
            self.logic.button_click("<-", self.animate_button_press)
        elif keysym == "Escape":
            self.logic.button_click("C", self.animate_button_press)
