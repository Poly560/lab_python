import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from time import time

fruits = ["ф1", "ф2", "ф3", "ф4", "ф5", "ф6", "ф7", "ф8", "ф9", "ф10"]
prices = {
    "ф1": 10,
    "ф2": 20,
    "ф3": 3,
    "ф4": 400,
    "ф5": 5,
    "ф6": 60,
    "ф7": 7,
    "ф8": 83,
    "ф9": 99,
    "ф10": 1055
}

def keep_all_menus(fruits, days):
    all_menus = []
    def create_a_menu(menu, day):
        if day == days:
            all_menus.append(menu.copy())
            return
        if day == days - 2 or day == days - 1:
            menu.append('ф2')
            create_a_menu(menu, day + 1)
            menu.pop()
        else:
            for f in fruits:
                menu.append(f)
                create_a_menu(menu, day + 1)
                menu.pop()
    create_a_menu([], 0)
    return all_menus

def target_function(menu, prices):
    return sum(prices[fruit] for fruit in menu)

def run_analysis():
    output_text.delete(1.0, tk.END)
    try:
        days = int(days_entry.get())
        if days < 3:
            raise ValueError("Количество дней должно быть не меньше 3")
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Неверное количество дней")
        return

    start_time = time()
    all_menus = keep_all_menus(fruits, days)
    min_cost = 10**10
    best_menu = None

    for menu in all_menus:
        cost = target_function(menu, prices)
        if cost < min_cost:
            min_cost = cost
            best_menu = menu

    end_time = time()
    recursiev_time = end_time - start_time

    output_text.insert(tk.END, f"Количество дней: {days}\n")
    output_text.insert(tk.END, f"Количество вариантов меню: {len(all_menus)}\n")
    output_text.insert(tk.END, f"Время выполнения: {recursiev_time:.6f} секунд\n\n")
    output_text.insert(tk.END, f"Самое бюджетное меню (стоимость {min_cost} руб.):\n{best_menu}\n\n")
    output_text.insert(tk.END, "Все варианты меню с их стоимостью:\n")

    for i, menu in enumerate(all_menus, 1):
        cost = target_function(menu, prices)
        output_text.insert(tk.END, f"{i}. {menu} - Стоимость: {cost} руб.\n")


root = tk.Tk()
root.title("Поиск бюджетного меню")
frame_input = ttk.Frame(root)
frame_input.pack(pady=5)
ttk.Label(frame_input, text="Количество дней (≥3):").pack(side=tk.LEFT, padx=5)
days_entry = ttk.Entry(frame_input, width=5)
days_entry.pack(side=tk.LEFT)
run_button = ttk.Button(root, text="Запустить анализ", command=run_analysis)
run_button.pack(pady=10)
output_text = scrolledtext.ScrolledText(root, width=80, height=30, wrap=tk.WORD)
output_text.pack(padx=10, pady=10)
root.mainloop()
