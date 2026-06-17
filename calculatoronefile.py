#калькулятор в одном файле
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageEnhance
from tkinter import  messagebox

memory_value = 0.0

root = tk.Tk()
root.title("My first Calculator")
root.geometry("360x540")
root.resizable(True, True)

# Переменные для отслеживания реального изменения размеров окна
last_width = 360
last_height = 540
buttons = [
    'MC', 'MR', 'M+', 'M-',
    'C', '()', '<-', '+',
    '7', '8', '9', '-',
    '4', '5', '6', '/',
    '1', '2', '3', '*',
    '+/-', '0', ',', '=',
]

def load_button_img(path_to_file):
    try:
        img = Image.open(path_to_file)
        return img
    except Exception as e:
        print(f"Не удалось загрузить {path_to_file}: {e}")
        return Image.new("RGB", (70, 70), "white")


# Загружаем оригиналы изображений (укажи свои пути)
digit_img = load_button_img(r"C:\Users\admin\OneDrive\Desktop\calculator 1000 str\images for calculator\babymonster asa _ SBS GAYO DAEJEON SUMMER 2025 (270725) (1).png")

operator_img = load_button_img(r"C:\Users\admin\OneDrive\Desktop\calculator 1000 str\images for calculator\загруженное (4) (1).png")
memory_img = load_button_img(r"C:\Users\admin\OneDrive\Desktop\calculator 1000 str\images for calculator\☆Wonhee☆ (1).png")



def resize_images(event=None):
    global last_width, last_height

    # Если событие вызвано не главным окном root, а кнопкой — игнорируем
    if event and event.widget != root:
        return

    current_width = root.winfo_width()
    current_height = root.winfo_height()

    # Проверяем, изменились ли размеры окна на самом деле
    if event and current_width == last_width and current_height == last_height:
        return

    # Запоминаем новые размеры
    last_width = current_width
    last_height = current_height

    # Вычисляем новый размер для кнопок на основе размеров окна
    btn_width = max(50, (current_width - 40) // 4)
    btn_height = max(40, (current_height - 100) // 7)

    def apply_resize(base_img, brightness_factor=1.0):
        img_resized = base_img.resize((btn_width, btn_height), Image.Resampling.LANCZOS)
        enhancer = ImageEnhance.Brightness(img_resized)
        img_bright = enhancer.enhance(brightness_factor)
        return ImageTk.PhotoImage(img_resized), ImageTk.PhotoImage(img_bright)

    for btn_text, btn in buttons_dict.items():
        if btn_text in ("MC", "MR", "M+", "M-"):
            base = memory_img
        elif btn_text in ("+", "-", "*", "/", "=", "C", "<-", "()"):
            base = operator_img
        else:
            base = digit_img

        normal_tk, dark_tk = apply_resize(base)
        # Затемняем вторую картинку для эффекта нажатия
        _, dark_tk = apply_resize(base, brightness_factor=0.6)

        # Перезаписываем картинки в словарь
        textures_dict[btn_text] = (normal_tk, dark_tk)
        btn.config(image=normal_tk)


# --- 2. ЛОГИКА КАЛЬКУЛЯТОРА ---
display = tk.Entry(root, font=("Arial", 22), justify="right",  width=14)
display.grid(row=0, column=0, columnspan=4, sticky="we", padx=15, pady=30)

buttons_dict = {}
textures_dict = {}


def safe_eval(expression):
    allowed = "0123456789+-*/(). "
    for ch in expression:
        if ch not in allowed: return "Error"
    try:
        return str(eval(expression))
    except ZeroDivisionError:
        return "Div by 0"
    except Exception:
        return "Error"


def button_click(char):
    global memory_value
    animate_button_press(char)
    display.config(state="normal")
    cursor_pos = display.index(tk.INSERT)

    if char == "MC":
        memory_value = 0.0
    elif char == "MR":
        val = int(memory_value) if memory_value.is_integer() else memory_value
        display.delete(0, tk.END)
        display.insert(tk.END, str(val))
    elif char == "M+":
        try:
            memory_value += float(display.get().replace(",", "."))
            display.delete(0, tk.END)
        except ValueError:
            pass
    elif char == "M-":
        try:
            memory_value -= float(display.get().replace(",", "."))
            display.delete(0, tk.END)
        except ValueError:
            pass
    elif char == ",":
        display.insert(cursor_pos, ".")
    elif char == '=':
        expr = display.get().replace(",", ".")
        result = safe_eval(expr)
        display.delete(0, tk.END)
        display.insert(tk.END, result)
    elif char == 'C':
        display.delete(0, tk.END)
    elif char == '<-':
        if cursor_pos > 0: display.delete(cursor_pos - 1)
    elif char == '+\\-':
        current = display.get()
        if current and current[0] == "-":
            display.delete(0, tk.END)
            display.insert(0, current[1:])
        elif current:
            display.delete(0, tk.END)
            display.insert(0, "-" + current)
    elif char == '()':
        display.insert(cursor_pos, "()")
        display.icursor(cursor_pos + 1)
    else:
        display.insert(cursor_pos, char)


def animate_button_press(btn_text):
    if btn_text in textures_dict and btn_text in buttons_dict:
        btn = buttons_dict[btn_text]
        normal_tex, dark_tex = textures_dict[btn_text]
        btn.config(image=dark_tex)
        root.after(100, lambda: btn.config(image=normal_tex))


def press_key(event):
    char = event.char
    keysym = event.keysym
    if char in "0123456789+-*/()":
        button_click(char)
        return "break"
    elif char in ",.":
        button_click(",")
        return "break"
    elif keysym == "Return":
        button_click("=")
        return "break"
    elif keysym == "BackSpace":
        button_click("<-")
        return "break"
    elif keysym == "Escape":
        button_click("C")
        return "break"
    return "break"


root.bind("<Key>", press_key)
display.bind("<Key>", press_key)

# --- 3. СОЗДАНИЕ КНОПОК ---
row_idx = 1
col_idx = 0

for btn_text in buttons:
    btn = tk.Button(
        root,
        text=btn_text,
        compound="center",
        fg="white",
        font=("Arial", 16, "bold"),
        borderwidth=0,
        relief="flat",
        highlightthickness=0,
        activebackground=root.cget("bg"),
        command=lambda b=btn_text: button_click(b)
    )
    btn.grid(row=row_idx, column=col_idx, padx=3, pady=3, sticky="nsew")
    buttons_dict[btn_text] = btn

    col_idx += 1
    if col_idx > 3:
        col_idx = 0
        row_idx += 1

# --- 4. НАСТРОЙКА АДАПТИВНОСТИ ---
for i in range(1, 8):
    root.rowconfigure(i, weight=1)
for i in range(4):
    root.columnconfigure(i, weight=1)

# Биндим событие изменения размеров окна
root.bind("<Configure>", resize_images)

# Инициализируем картинки при первом запуске
root.update()
resize_images()

root.mainloop()
