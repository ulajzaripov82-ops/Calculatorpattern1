# utils.py
import ast
import operator
from PIL import Image, ImageTk, ImageEnhance, ImageOps



#импорт  нужной библиотеки
def load_button_img(path_to_file):
    """Загружает изображение, если не получается — возвращает белую заглушку."""
    try:
        img = Image.open(path_to_file)
        return img
    except Exception as e:
        print(f"Не удалось загрузить {path_to_file}: {e}")
        return Image.new("RGBA", (70, 70), (255, 255, 255, 255))


def resize_image(base_img, width, height, brightness=1.0):
    """Подгоняет изображение под размер и изменяет яркость."""
    img_fitted = ImageOps.fit(base_img, (width, height), Image.Resampling.BICUBIC)
    enhancer = ImageEnhance.Brightness(img_fitted)
    img_final = enhancer.enhance(brightness)
    return ImageTk.PhotoImage(img_final)


def safe_eval(expression):
    # Добавляем буквы и знаки в разрешенные (убрали '*', так как она есть в '**')
    allowed = "0123456789+-*/()."

    # Если пользователь ввел '**' или '**' где-либо в выражении
    if "**" in expression:
        return "Error: invalid character"
    elif "//" in expression:
        return "Eror:invalid character"

        # Проверка на наличие других недопустимых символов
    for ch in expression:
        if ch not in allowed:
            return "Error: invalid character"

    try:
        return str(eval(expression))
    except ZeroDivisionError:
        return "Div by 0"
    except Exception:
        return "Error"





