import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

class Rectangle:
    def __init__(self, x1, y1, x2, y2, color="white"):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        if self.x1 > self.x2:
            self.x1, self.x2 = self.x2, self.x1
        if self.y1 > self.y2:
            self.y1, self.y2 = self.y2, self.y1
    
    def intersects(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)
    
    def move(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy
    
    def change_color(self, new_color):
        self.color = new_color


class RectangleVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Прямоугольники")
        self.rectangles = []
        self.selected_rect = None
        self.setup_gui()
    
    def setup_gui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(main_frame, width=600, height=400, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=5, pady=5)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        ttk.Button(control_frame, text="Добавить файл", command=self.load_from_csv).pack(pady=5, fill=tk.X)
        ttk.Button(control_frame, text="Проверить пересечения", command=self.check_intersections).pack(pady=5, fill=tk.X)
        ttk.Button(control_frame, text="Изменить цвет", command=self.change_color_dialog).pack(pady=5, fill=tk.X)
        ttk.Button(control_frame, text="Переместить", command=self.move_dialog).pack(pady=5, fill=tk.X)
        self.rect_listbox = tk.Listbox(control_frame, width=40, height=15)
        self.rect_listbox.pack(pady=5, fill=tk.BOTH, expand=True)
        self.rect_listbox.bind("<<ListboxSelect>>", self.on_rect_select)
    
    def load_from_csv(self):
        filename = filedialog.askopenfilename(
            title="Выберите CSV файл с прямоугольниками",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not filename:
            return
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                self.rectangles = []
                for row in reader:
                    if len(row) >= 4:
                        try:
                            x1, y1, x2, y2 = map(int, row[:4])
                            color = row[4].strip() if len(row) > 4 and row[4].strip() else "white"
                            self.rectangles.append(Rectangle(x1, y1, x2, y2, color))
                        except ValueError:
                            continue
                
                if self.rectangles:
                    self.update_rect_list()
                    self.draw_rectangles()
                else:
                    messagebox.showwarning("Предупреждение", "В файле нет необходимых данных")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {str(e)}")
    
    def change_color_dialog(self):
        if not self.selected_rect:
            messagebox.showwarning("Предупреждение", "Выберите прямоугольник из списка")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Изменить цвет")
        ttk.Label(dialog, text="Выберите цвет:").pack(pady=10)
        color_var = tk.StringVar(value=self.selected_rect.color)
        color_combo = ttk.Combobox(dialog, textvariable=color_var, values=["red", "blue", "green", "yellow", "orange", "purple", "black", "white", "gray", "brown"])
        color_combo.pack(pady=5)
        
        def change_color():
            self.selected_rect.change_color(color_var.get())
            self.draw_rectangles()
            dialog.destroy()
        
        ttk.Button(dialog, text="Применить", command=change_color).pack(pady=10)
    
    def move_dialog(self):
        if not self.selected_rect:
            messagebox.showwarning("Предупреждение", "Выберите прямоугольник из списка")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Переместить прямоугольник")
        ttk.Label(dialog, text="Смещение по X:").grid(row=0, column=0, padx=5, pady=5)
        dx_entry = ttk.Entry(dialog)
        dx_entry.grid(row=0, column=1, padx=5, pady=5)
        dx_entry.insert(0, "0")
        ttk.Label(dialog, text="Смещение по Y:").grid(row=1, column=0, padx=5, pady=5)
        dy_entry = ttk.Entry(dialog)
        dy_entry.grid(row=1, column=1, padx=5, pady=5)
        dy_entry.insert(0, "0")
        
        def move_rect():
            try:
                dx = int(dx_entry.get())
                dy = int(dy_entry.get())
                self.selected_rect.move(dx, dy)
                self.draw_rectangles()
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректные значения")
        
        ttk.Button(dialog, text="Переместить", command=move_rect).grid(row=2, column=0, columnspan=2, pady=10)
    
    def check_intersections(self):
        if len(self.rectangles) < 2:
            messagebox.showinfo("Информация", "Недостаточно прямоугольников для проверки пересечений")
            return
        
        result = "Результаты проверки пересечений:\n\n"
        intersections_found = False
        
        for i, rect1 in enumerate(self.rectangles):
            for j, rect2 in enumerate(self.rectangles):
                if i < j and rect1.intersects(rect2):
                    result += f"Прямоугольник {i+1} пересекается с прямоугольником {j+1}\n"
                    intersections_found = True
        
        if not intersections_found:
            result += "Пересечений не найдено"
        
        messagebox.showinfo("Проверка пересечений", result)
    
    def draw_rectangles(self):
        self.canvas.delete("all")
        for x in range(0, 600, 50):
            self.canvas.create_line(x, 0, x, 400, fill="lightgray")
        for y in range(0, 400, 50):
            self.canvas.create_line(0, y, 600, y, fill="lightgray")
        
        self.canvas.create_line(0, 200, 600, 200, fill="black", width=2) 
        self.canvas.create_line(300, 0, 300, 400, fill="black", width=2) 
        
        for x in range(0, 600, 50):
            label_value = (x - 300) // 10  
            if label_value != 0:
                self.canvas.create_text(x, 210, text=f"{label_value}", fill="black", font=("Arial", 8))
        
        for y in range(0, 400, 50):
            label_value = (200 - y) // 10 
            if label_value != 0:  
                self.canvas.create_text(290, y, text=f"{label_value}", fill="black", font=("Arial", 8), anchor="e")
        
        self.canvas.create_text(590, 190, text="X", fill="black", font=("Arial", 10, "bold"))
        self.canvas.create_text(310, 10, text="Y", fill="black", font=("Arial", 10, "bold"))
        self.canvas.create_text(310, 210, text="0", fill="black", font=("Arial", 8))
        
        for i, rect in enumerate(self.rectangles):
            x1 = 300 + rect.x1 * 10
            y1 = 200 - rect.y1 * 10
            x2 = 300 + rect.x2 * 10
            y2 = 200 - rect.y2 * 10
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=rect.color, outline="black", width=2)
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2 
            text_color = "white" if rect.color in ["black", "blue", "red", "green", "purple", "brown"] else "black"
            self.canvas.create_text(center_x, center_y, text=str(i+1), fill=text_color, font=("Impact", 10, "normal"))
    
    def update_rect_list(self):
        self.rect_listbox.delete(0, tk.END)
        for i, rect in enumerate(self.rectangles):
            self.rect_listbox.insert(tk.END, f"Прямоугольник {i+1}: ({rect.x1},{rect.y1})-({rect.x2},{rect.y2})")
    
    def on_rect_select(self, event):
        selection = self.rect_listbox.curselection()
        if selection:
            index = selection[0]
            self.selected_rect = self.rectangles[index]
    
    def on_canvas_click(self, event):
        sys_x = (event.x - 300) // 10
        sys_y = (200 - event.y) // 10
        
        for i, rect in enumerate(self.rectangles):
            if (rect.x1 <= sys_x <= rect.x2 and rect.y1 <= sys_y <= rect.y2):
                self.rect_listbox.selection_clear(0, tk.END)
                self.rect_listbox.selection_set(i)
                self.selected_rect = rect
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = RectangleVisualizer(root)
    root.mainloop()