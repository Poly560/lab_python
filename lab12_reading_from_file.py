import tkinter as tk
from tkinter import messagebox, filedialog
import random

class BattleShipGame:
    def __init__(self):
        self._init_game_state()
        self.root = tk.Tk()
        self.root.title("Морской бой")
        self.setup_ui()
        self.setup_robot_ships()

    def _init_game_state(self):
        self.player_matrix = [[0 for j in range(10)] for i in range(10)]
        self.robot_matrix = [[0 for j in range(10)] for i in range(10)]
        self.player_hits = [[0 for j in range(10)] for i in range(10)]
        self.robot_hits = [[0 for j in range(10)] for i in range(10)]
        self.l = len(self.player_matrix)
        self.letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К']
        self.robot_last_hit = None
        self.robot_hit_direction = None
        self.all_ships_placed = False

    def new_game(self):
        self._init_game_state()
        for entries in self.single_deck_entries:
            for entry in entries:
                entry.delete(0, tk.END)
        for entries in self.double_deck_entries:
            for entry in entries:
                entry.delete(0, tk.END)
        for entries in self.triple_deck_entries:
            for entry in entries:
                entry.delete(0, tk.END)
        self.quadruple_x1_entry.delete(0, tk.END)
        self.quadruple_y1_entry.delete(0, tk.END)
        self.quadruple_x2_entry.delete(0, tk.END)
        self.quadruple_y2_entry.delete(0, tk.END)
        self.setup_robot_ships()
        self.update_display()
        messagebox.showinfo("Новая игра", "Игра сброшена! Разместите свои корабли и начинайте!")

    def setup_robot_ships(self):
        ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        for ship_length in ships:
            placed = False
            attempts = 0
            while not placed and attempts < 100:
                attempts += 1
                direction = random.randint(0, 1)
                if direction == 0:
                    x = random.randint(0, 9)
                    y = random.randint(0, 10 - ship_length)
                    x2 = x
                    y2 = y + ship_length - 1
                else:
                    x = random.randint(0, 10 - ship_length)
                    y = random.randint(0, 9)
                    x2 = x + ship_length - 1
                    y2 = y
                if self.is_valid_ship_position(self.robot_matrix, x, y, x2, y2, ship_length):
                    self.place_ship(self.robot_matrix, x, y, x2, y2)
                    placed = True
            if not placed:
                self.robot_matrix = [[0 for _ in range(10)] for _ in range(10)]
                return self.setup_robot_ships()

    def convert_coordinate(self, coord, expected_type=None):
        if isinstance(coord, str):
            coord = coord.upper().strip()
            if not coord:
                return None
            if expected_type == 'letter' or (len(coord) == 1 and coord.isalpha()):
                if coord in self.letters:
                    return self.letters.index(coord)
            elif expected_type == 'number' or coord.isdigit():
                if coord.isdigit():
                    num = int(coord)
                    if 1 <= num <= 10:
                        return num - 1
        elif isinstance(coord, int):
            if 1 <= coord <= 10:
                return coord - 1
        return None
    
    def is_valid_ship_position(self, m, x1, y1, x2=None, y2=None, ship_length=None):
        x1, y1 = (self.convert_coordinate(x1), self.convert_coordinate(y1)) if not isinstance(x1, int) else (x1, y1)
        if any(c is None for c in (x1, y1)):
            return False
        
        if x2 is None and y2 is None:
            return (0 <= x1 < self.l and 0 <= y1 < self.l and 
                    not any(m[i][j] == 1 for i in range(max(0, x1-1), min(10, x1+2)) 
                                        for j in range(max(0, y1-1), min(10, y1+2))))
        
        x2, y2 = (self.convert_coordinate(x2), self.convert_coordinate(y2)) if not isinstance(x2, int) else (x2, y2)
        if any(c is None for c in (x2, y2)):
            return False
        
        x1, x2, y1, y2 = sorted([x1, x2])[0], sorted([x1, x2])[1], sorted([y1, y2])[0], sorted([y1, y2])[1]
        return (0 <= x1 <= x2 < self.l and 0 <= y1 <= y2 < self.l and
                ((x1 == x2) or (y1 == y2)) and
                (ship_length is None or (max(x2-x1, y2-y1) + 1 == ship_length)) and
                (max(x2-x1, y2-y1) + 1 <= 4) and
                not any(m[i][j] == 1 for i in range(max(0, x1-1), min(10, x2+2))
                                    for j in range(max(0, y1-1), min(10, y2+2))))

    def place_ship(self, m, x1, y1, x2=None, y2=None):
        if isinstance(x1, int) and isinstance(y1, int):
            x1_num, y1_num = x1, y1
        else:
            x1_num = self.convert_coordinate(x1)
            y1_num = self.convert_coordinate(y1)
        if x1_num is None or y1_num is None:
            return False
        if x2 is None or y2 is None:
            m[x1_num][y1_num] = 1
            return True
        if isinstance(x2, int) and isinstance(y2, int):
            x2_num, y2_num = x2, y2
        else:
            x2_num = self.convert_coordinate(x2)
            y2_num = self.convert_coordinate(y2)
        if x2_num is None or y2_num is None:
            return False
        if y1_num == y2_num:
            for i in range(x1_num, x2_num + 1):
                m[i][y1_num] = 1
        else:
            for j in range(y1_num, y2_num + 1):
                m[x1_num][j] = 1
        return True

    def update_display(self):
        for i in range(self.l):
            for j in range(self.l):
                if self.player_matrix[i][j] == 1 and self.robot_hits[i][j] == 1:
                    self.player_cells[i][j].config(text="X", bg="red")
                elif self.robot_hits[i][j] == 1:
                    self.player_cells[i][j].config(text="•", bg="yellow")
                elif self.player_matrix[i][j] == 1:
                    self.player_cells[i][j].config(text="■", bg="gray")
                else:
                    self.player_cells[i][j].config(text="·", bg="#E0F0FF")
        for i in range(self.l):
            for j in range(self.l):
                if self.player_hits[i][j] == 1 and self.robot_matrix[i][j] == 1:
                    self.robot_cells[i][j].config(text="X", bg="red")
                elif self.player_hits[i][j] == 1:
                    self.robot_cells[i][j].config(text="•", bg="yellow")
                else:
                    self.robot_cells[i][j].config(text="·", bg="#E0F0FF")

    def place_ship_from_entries(self, entries, ship_length=None):
        coords = []
        for i, entry in enumerate(entries):
            expected_type = 'letter' if i % 2 == 0 else 'number'
            coord = self.convert_coordinate(entry.get().strip(), expected_type)
            if entry.get().strip() and coord is None:
                return 'invalid'
            coords.append(coord)
        if not any(coord is not None for coord in coords):
            return None
        if any(coord is None for coord in coords):
            return 'invalid'
        if len(coords) == 2:
            x, y = coords
            if self.is_valid_ship_position(self.player_matrix, x, y, ship_length=ship_length):
                return self.place_ship(self.player_matrix, x, y)
        else:
            x1, y1, x2, y2 = coords
            if self.is_valid_ship_position(self.player_matrix, x1, y1, x2, y2, ship_length=ship_length):
                return self.place_ship(self.player_matrix, x1, y1, x2, y2)
        return 'invalid'

    def check_all_ships_placed(self):
        ship_cells_count = sum(cell == 1 for row in self.player_matrix for cell in row)
        return ship_cells_count == 20
    
    def place_ships(self):
        self.player_matrix = [[0 for _ in range(self.l)] for _ in range(self.l)]
        self.all_ships_placed = False
        for i, entries in enumerate(self.single_deck_entries):
            result = self.place_ship_from_entries(entries)
            if result == 'invalid':
                messagebox.showerror("Ошибка", f"1-палубный корабль {i+1} имеет некорректные координаты!\nИспользуйте формат: буква(А-К) цифра(1-10)")
                self.player_matrix = [[0 for _ in range(self.l)] for _ in range(self.l)]
                return
        for i, entries in enumerate(self.double_deck_entries):
            result = self.place_ship_from_entries(entries, 2)
            if result == 'invalid':
                messagebox.showerror("Ошибка", f"2-палубный корабль {i+1} имеет некорректные координаты!\nИспользуйте формат: буква(А-К) цифра(1-10)")
                self.player_matrix = [[0 for _ in range(self.l)] for _ in range(self.l)]
                return
        for i, entries in enumerate(self.triple_deck_entries):
            result = self.place_ship_from_entries(entries, 3)
            if result == 'invalid':
                messagebox.showerror("Ошибка", f"3-палубный корабль {i+1} имеет некорректные координаты!\nИспользуйте формат: буква(А-К) цифра(1-10)")
                self.player_matrix = [[0 for _ in range(self.l)] for _ in range(self.l)]
                return
        entries = (self.quadruple_x1_entry, self.quadruple_y1_entry, self.quadruple_x2_entry, self.quadruple_y2_entry)
        result = self.place_ship_from_entries(entries, 4)
        if result == 'invalid':
            messagebox.showerror("Ошибка", "4-палубный корабль имеет некорректные координаты!\nИспользуйте формат: буква(А-К) цифра(1-10)")
            self.player_matrix = [[0 for _ in range(self.l)] for _ in range(self.l)]
            return
        if not self.check_all_ships_placed():
            messagebox.showerror("Ошибка", "Расставлены не все корабли!.")
            self.player_matrix = [[0 for _ in range(self.l)] for _ in range(self.l)]
            self.all_ships_placed = False
            return
        
        messagebox.showinfo("Успех", "Корабли успешно размещены! Можете начинать игру.")
        self.all_ships_placed = True
        self.update_display()

    def player_attack(self, x, y):
        if not self.all_ships_placed:
            messagebox.showwarning("Не готово", "Сначала разместите все свои корабли!")
            return
        if self.player_hits[x][y] != 0:
            return
        self.player_hits[x][y] = 1
        if self.robot_matrix[x][y] == 1:
            # messagebox.showinfo("Попадание!", f"Вы попали в корабль противника! ({self.letters[x]}{y+1})")
            hit_again = True
            ship_sunk = self.check_ship_sunk(self.robot_matrix, self.player_hits, x, y)
            if ship_sunk:
                # messagebox.showinfo("Потоплен!", "Вы потопили корабль противника!")
                self.mark_sunk_ship_neighbors(self.robot_matrix, self.player_hits, x, y)
                hit_again = False
            self.update_display()
            if self.check_game_over():
                return
            if hit_again:
                return
            else:
                self.root.after(500, self.robot_attack)
        else:
            self.update_display()
            if self.check_game_over():
                return
            self.root.after(500, self.robot_attack)

    def robot_attack(self):
        x, y = self.get_robot_target()
        self.robot_hits[x][y] = 1
        if self.player_matrix[x][y] == 1:
            self.robot_last_hit = (x, y)
            # messagebox.showinfo("Робот атакует", f"Робот попал в ваш корабль! ({self.letters[x]}{y+1})")
            hit_again = True
            ship_sunk = self.check_ship_sunk(self.player_matrix, self.robot_hits, x, y)
            if ship_sunk:
                # messagebox.showinfo("Робот атакует", "Робот потопил ваш корабль!")
                self.mark_sunk_ship_neighbors(self.player_matrix, self.robot_hits, x, y)
                self.robot_last_hit = None
                self.robot_hit_direction = None
                hit_again = False
            self.update_display()
            if self.check_game_over():
                return
            if hit_again:
                self.root.after(500, self.robot_attack)
        else:
            if self.robot_hit_direction is not None:
                self.robot_hit_direction = None
            self.update_display()
            if self.check_game_over():
                return

    def mark_sunk_ship_neighbors(self, ship_matrix, hits_matrix, x, y):
        ship_cells = []
        visited = set()
        def find_ship_cells(i, j):
            if (i, j) in visited or not (0 <= i < 10 and 0 <= j < 10):
                return
            visited.add((i, j))
            if ship_matrix[i][j] == 1:
                ship_cells.append((i, j))
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    find_ship_cells(i + dx, j + dy)
        find_ship_cells(x, y)
        for cell_x, cell_y in ship_cells:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = cell_x + dx, cell_y + dy
                    if 0 <= nx < 10 and 0 <= ny < 10 and hits_matrix[nx][ny] == 0:
                        hits_matrix[nx][ny] = 1

    def get_robot_target(self):
        if self.robot_last_hit is not None:
            x, y = self.robot_last_hit
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            if self.robot_hit_direction is None:
                for dx, dy in directions:
                    new_x, new_y = x + dx, y + dy
                    if (0 <= new_x < 10 and 0 <= new_y < 10 and self.robot_hits[new_x][new_y] == 0):
                        self.robot_hit_direction = (dx, dy)
                        return new_x, new_y
            else:
                dx, dy = self.robot_hit_direction
                new_x, new_y = x + dx, y + dy
                if (0 <= new_x < 10 and 0 <= new_y < 10 and self.robot_hits[new_x][new_y] == 0):
                    return new_x, new_y
                else:
                    self.robot_hit_direction = None
                    for dx, dy in directions:
                        new_x, new_y = x + dx, y + dy
                        if (0 <= new_x < 10 and 0 <= new_y < 10 and self.robot_hits[new_x][new_y] == 0):
                            self.robot_hit_direction = (dx, dy)
                            return new_x, new_y
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            if self.robot_hits[x][y] == 0:
                return x, y

    def check_ship_sunk(self, ship_matrix, hits_matrix, x, y):
        ship_cells = []
        visited = set()
        def find_ship_cells(i, j):
            if (i, j) in visited or not (0 <= i < 10 and 0 <= j < 10):
                return
            visited.add((i, j))
            if ship_matrix[i][j] == 1:
                ship_cells.append((i, j))
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    find_ship_cells(i + dx, j + dy)
        find_ship_cells(x, y)
        for cell_x, cell_y in ship_cells:
            if hits_matrix[cell_x][cell_y] != 1:
                return False
        return True

    def check_game_over(self):
        player_wins = all(cell == 0 or self.player_hits[i][j] == 1 for i, row in enumerate(self.robot_matrix) for j, cell in enumerate(row) if cell == 1)
        robot_wins = all(cell == 0 or self.robot_hits[i][j] == 1 for i, row in enumerate(self.player_matrix) for j, cell in enumerate(row) if cell == 1)
        if player_wins:
            messagebox.showinfo("Игра окончена", "Поздравляем! Вы выиграли!")
            return True
        elif robot_wins:
            messagebox.showinfo("Игра окончена", "Робот выиграл! Попробуйте еще раз.")
            return True
        return False
    
    def fill_input_fields_from_matrix(self):
        all_entries = (self.single_deck_entries + self.double_deck_entries + self.triple_deck_entries + [[self.quadruple_x1_entry, self.quadruple_y1_entry, self.quadruple_x2_entry, self.quadruple_y2_entry]])
        for entries in all_entries:
            for entry in entries:
                entry.delete(0, tk.END)
        ships = self.extract_ships_from_matrix()
        ship_types = {
            1: (self.single_deck_entries, 4),
            2: (self.double_deck_entries, 3), 
            3: (self.triple_deck_entries, 2),
            4: ([None], 1)
        }
        for size, (entries_list, max_count) in ship_types.items():
            ships_of_type = [ship for ship in ships if len(ship) == size][:max_count]
            
            for i, ship in enumerate(ships_of_type):
                if size == 4:
                    x1, y1 = ship[0]
                    x2, y2 = ship[-1]
                    self.quadruple_x1_entry.insert(0, self.letters[x1])
                    self.quadruple_y1_entry.insert(0, str(y1 + 1))
                    self.quadruple_x2_entry.insert(0, self.letters[x2])
                    self.quadruple_y2_entry.insert(0, str(y2 + 1))
                elif i < len(entries_list):
                    x1, y1 = ship[0]
                    x2, y2 = ship[-1]
                    entries = entries_list[i]
                    entries[0].insert(0, self.letters[x1])
                    entries[1].insert(0, str(y1 + 1))
                    if size > 1:
                        entries[2].insert(0, self.letters[x2])
                        entries[3].insert(0, str(y2 + 1))

    def extract_ships_from_matrix(self):
        visited = set()
        ships = []
        
        def find_ship(x, y):
            ship = [(x, y)]
            visited.add((x, y))
            for dx, dy in [(0, 1), (1, 0)]:
                nx, ny = x + dx, y + dy
                while (0 <= nx < 10 and 0 <= ny < 10 and 
                    self.player_matrix[nx][ny] == 1 and 
                    (nx, ny) not in visited):
                    visited.add((nx, ny))
                    ship.append((nx, ny))
                    nx += dx
                    ny += dy
            
            return sorted(ship)
        
        for i in range(10):
            for j in range(10):
                if self.player_matrix[i][j] == 1 and (i, j) not in visited:
                    ships.append(find_ship(i, j))
        
        return ships

    def load_ships_from_file(self):
        filename = filedialog.askopenfilename(title="Выберите файл с расстановкой кораблей", filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")])
        if not filename:
            return
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            self.player_matrix = [[0 for _ in range(self.l)] for _ in range(self.l)]
            ships_placed = 0
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                coords = line.split()
                if len(coords) == 2:
                    x, y = coords
                    x_num = self.convert_coordinate(x, 'letter')
                    y_num = self.convert_coordinate(y, 'number')
                    if (x_num is not None and y_num is not None and 
                        self.is_valid_ship_position(self.player_matrix, x_num, y_num)):
                        self.place_ship(self.player_matrix, x_num, y_num)
                        ships_placed += 1
                        
                elif len(coords) == 4:
                    x1, y1, x2, y2 = coords
                    x1_num = self.convert_coordinate(x1, 'letter')
                    y1_num = self.convert_coordinate(y1, 'number')
                    x2_num = self.convert_coordinate(x2, 'letter')
                    y2_num = self.convert_coordinate(y2, 'number')
                    if (x1_num is not None and y1_num is not None and 
                        x2_num is not None and y2_num is not None and
                        self.is_valid_ship_position(self.player_matrix, x1_num, y1_num, x2_num, y2_num)):
                        self.place_ship(self.player_matrix, x1_num, y1_num, x2_num, y2_num)
                        ships_placed += 1
            
            if ships_placed > 0:
                self.all_ships_placed = self.check_all_ships_placed()
                self.fill_input_fields_from_matrix()
                self.update_display()
                messagebox.showinfo("Успех", f"Загружено {ships_placed} кораблей из файла!")
            else:
                messagebox.showwarning("Предупреждение", "Не удалось загрузить корабли из файла!")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при чтении файла: {str(e)}")

    def setup_ui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)
        fields_frame = tk.Frame(main_frame)
        fields_frame.grid(row=0, column=0, padx=10)
        player_frame = tk.Frame(fields_frame)
        player_frame.grid(row=0, column=0, padx=10)
        tk.Label(player_frame, text="Ваше поле", font=("Arial", 12, "bold")).pack()
        self.player_field_frame = tk.Frame(player_frame)
        self.player_field_frame.pack()
        robot_frame = tk.Frame(fields_frame)
        robot_frame.grid(row=0, column=1, padx=10)
        tk.Label(robot_frame, text="Поле противника", font=("Arial", 12, "bold")).pack()
        self.robot_field_frame = tk.Frame(robot_frame)
        self.robot_field_frame.pack()
        self.input_frame = tk.Frame(main_frame)
        self.input_frame.grid(row=0, column=1, padx=10)
        self.create_game_fields()
        self.create_ship_input_panel()
        new_game_button = tk.Button(fields_frame, text="Новая игра", command=self.new_game, font=("Arial", 12, "bold"), padx=20, pady=10)
        new_game_button.grid(row=1, column=0, columnspan=2, pady=20)
        load_button = tk.Button(self.input_frame, text="Загрузить из файла", command=self.load_ships_from_file)
        load_button.grid(row=15, column=0, columnspan=6, pady=5)
        
    def create_game_fields(self):
        self.player_cells = []
        for i in range(self.l + 1):
            for j in range(self.l + 1):
                if i == 0 and j == 0:
                    continue
                elif i == 0:
                    label = tk.Label(self.player_field_frame, text=str(j), width=3, height=1)
                    label.grid(row=0, column=j)
                elif j == 0:
                    label = tk.Label(self.player_field_frame, text=self.letters[i-1], width=3, height=1)
                    label.grid(row=i, column=0)
        for i in range(self.l):
            row = []
            for j in range(self.l):
                cell = tk.Label(self.player_field_frame, text="·", width=3, height=1, relief="raised", bg="#E0F0FF")
                cell.grid(row=i+1, column=j+1)
                row.append(cell)
            self.player_cells.append(row)
        self.robot_cells = []
        for i in range(self.l + 1):
            for j in range(self.l + 1):
                if i == 0 and j == 0:
                    continue
                elif i == 0:
                    label = tk.Label(self.robot_field_frame, text=str(j), width=3, height=1)
                    label.grid(row=0, column=j)
                elif j == 0:
                    label = tk.Label(self.robot_field_frame, text=self.letters[i-1], width=3, height=1)
                    label.grid(row=i, column=0)
        for i in range(self.l):
            row = []
            for j in range(self.l):
                cell = tk.Label(self.robot_field_frame, text="·", width=3, height=1, relief="raised", bg="#E0F0FF")
                cell.grid(row=i+1, column=j+1)
                cell.bind('<Button-1>', lambda e, x=i, y=j: self.player_attack(x, y))
                row.append(cell)
            self.robot_cells.append(row)

    def create_ship_input_panel(self):
        tk.Label(self.input_frame, text="1-палубные корабли (4 шт):", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 5))
        self.single_deck_entries = []
        for i in range(4):
            row_frame = tk.Frame(self.input_frame)
            row_frame.grid(row=i+1, column=0, columnspan=3, pady=2)
            tk.Label(row_frame, text=f"Корабль {i+1}:").grid(row=0, column=0)
            x_entry = tk.Entry(row_frame, width=3)
            x_entry.grid(row=0, column=1, padx=2)
            y_entry = tk.Entry(row_frame, width=3)
            y_entry.grid(row=0, column=2, padx=2)
            self.single_deck_entries.append((x_entry, y_entry))
        tk.Label(self.input_frame, text="\n2-палубные корабли (3 шт):", font=("Arial", 10, "bold")).grid(row=5, column=0, columnspan=5, sticky="w", pady=(10, 5))
        self.double_deck_entries = []
        for i in range(3):
            row_frame = tk.Frame(self.input_frame)
            row_frame.grid(row=i+6, column=0, columnspan=5, pady=2)
            tk.Label(row_frame, text=f"Корабль {i+1}:").grid(row=0, column=0)
            x1_entry = tk.Entry(row_frame, width=3)
            x1_entry.grid(row=0, column=1, padx=2)
            y1_entry = tk.Entry(row_frame, width=3)
            y1_entry.grid(row=0, column=2, padx=2)
            tk.Label(row_frame, text="-").grid(row=0, column=3)
            x2_entry = tk.Entry(row_frame, width=3)
            x2_entry.grid(row=0, column=4, padx=2)
            y2_entry = tk.Entry(row_frame, width=3)
            y2_entry.grid(row=0, column=5, padx=2)
            self.double_deck_entries.append((x1_entry, y1_entry, x2_entry, y2_entry))
        tk.Label(self.input_frame, text="\n3-палубные корабли (2 шт):", font=("Arial", 10, "bold")).grid(row=9, column=0, columnspan=5, sticky="w", pady=(10, 5))
        self.triple_deck_entries = []
        for i in range(2):
            row_frame = tk.Frame(self.input_frame)
            row_frame.grid(row=i+10, column=0, columnspan=5, pady=2)
            tk.Label(row_frame, text=f"Корабль {i+1}:").grid(row=0, column=0)
            x1_entry = tk.Entry(row_frame, width=3)
            x1_entry.grid(row=0, column=1, padx=2)
            y1_entry = tk.Entry(row_frame, width=3)
            y1_entry.grid(row=0, column=2, padx=2)
            tk.Label(row_frame, text="-").grid(row=0, column=3)
            x2_entry = tk.Entry(row_frame, width=3)
            x2_entry.grid(row=0, column=4, padx=2)
            y2_entry = tk.Entry(row_frame, width=3)
            y2_entry.grid(row=0, column=5, padx=2)
            self.triple_deck_entries.append((x1_entry, y1_entry, x2_entry, y2_entry))
        tk.Label(self.input_frame, text="\n4-палубный корабль (1 шт):", font=("Arial", 10, "bold")).grid(row=12, column=0, columnspan=5, sticky="w", pady=(10, 5))
        row_frame = tk.Frame(self.input_frame)
        row_frame.grid(row=13, column=0, columnspan=5, pady=2)
        tk.Label(row_frame, text="Корабль 1:").grid(row=0, column=0)
        self.quadruple_x1_entry = tk.Entry(row_frame, width=3)
        self.quadruple_x1_entry.grid(row=0, column=1, padx=2)
        self.quadruple_y1_entry = tk.Entry(row_frame, width=3)
        self.quadruple_y1_entry.grid(row=0, column=2, padx=2)
        tk.Label(row_frame, text="-").grid(row=0, column=3)
        self.quadruple_x2_entry = tk.Entry(row_frame, width=3)
        self.quadruple_x2_entry.grid(row=0, column=4, padx=2)
        self.quadruple_y2_entry = tk.Entry(row_frame, width=3)
        self.quadruple_y2_entry.grid(row=0, column=5, padx=2)
        place_button = tk.Button(self.input_frame, text="Разместить корабли", command=self.place_ships)
        place_button.grid(row=14, column=0, columnspan=6, pady=10)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = BattleShipGame()
    game.run()
