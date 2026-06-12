# logic.py
import tkinter as tk          # ← ЭТОТ ИМПОРТ БЫЛ ОТСУТСТВОВАут
from utils import safe_eval


class CalculatorLogic:
    def __init__(self, display_widget):
        self.display = display_widget
        self.memory = 0.0

    def button_click(self, char, animate_callback=None):
        if animate_callback:
            animate_callback(char)

        cursor_pos = self.display.index(tk.INSERT)   # теперь tk.INSERT определён

        # --- остальной код без изменений ---
        if char == "MC":
            self.memory = 0.0
        elif char == "MR":
            val = int(self.memory) if self.memory.is_integer() else self.memory
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(val))
        elif char == "M+":
            try:
                self.memory += float(self.display.get().replace(",", "."))
            except ValueError:
                pass
        elif char == "M-":
            try:
                self.memory -= float(self.display.get().replace(",", "."))
            except ValueError:
                pass
        elif char == ",":
            self.display.insert(cursor_pos, ".")
        elif char == "=":
            expr = self.display.get().replace(",", ".")
            result = safe_eval(expr)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, result)
        elif char == "C":
            self.display.delete(0, tk.END)
        elif char == "<-":
            if cursor_pos > 0:
                self.display.delete(cursor_pos - 1)
        elif char == "+/-":
            current = self.display.get()
            if current and current[0] == "-":
                self.display.delete(0, tk.END)
                self.display.insert(0, current[1:])
            elif current:
                self.display.delete(0, tk.END)
                self.display.insert(0, "-" + current)
        elif char == "()":
            self.display.insert(cursor_pos, "()")
            self.display.icursor(cursor_pos + 1)
        else:
            self.display.insert(cursor_pos, char)
