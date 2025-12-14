import tkinter as tk
from tkinter import messagebox
import random

class MazeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Выход из лабиринта")
        self.root.geometry("900x700")
        self.rows = 15
        self.cols = 15
        self.cell_size = 35
        self.robot_radius_ratio = 0.4
        self.maze = []
        self.robot_pos = None
        self.exits = []
        self.path = []
        self.path_rects = []
        self.robot_circle = None
        self.exit_count = tk.IntVar(value=1)
        self.found_exits = set()
        self.start_pos = (7, 7)
        self.colors = {
            'wall': '#353954',
            'path': 'white',
            'robot': "#417ec4",
            'start': '#f25275',
            'exit': '#ffcc00',
            'route': '#bdc6ff',
            'found_exit': '#98c441'
        }
        
        self.create_main_menu()
        self.initialize_game()
    
    def create_main_menu(self):
        menu_frame = tk.Frame(self.root, bg='#a7add4', height=100)
        menu_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        container_frame = tk.Frame(menu_frame, bg='#a7add4')
        container_frame.place(relx=0.5, rely=0.5, anchor='center')
        build_btn = tk.Button(container_frame, text="Построить новый лабиринт", command=self.build_maze, font=('Arial', 12))
        build_btn.pack(side=tk.LEFT, padx=10, pady=10)
        self.solve_reset_btn = tk.Button(container_frame, text="Найти выход", command=self.solve_or_reset_maze, font=('Arial', 12))
        self.solve_reset_btn.pack(side=tk.LEFT, padx=10, pady=10)
        exit_label = tk.Label(container_frame, text="Выходы:", font=('Arial', 12))
        exit_label.pack(side=tk.LEFT, padx=(20, 5), pady=10)
        exit_spin = tk.Spinbox(container_frame, from_=1, to=5, width=5, textvariable=self.exit_count, font=('Arial', 12))
        exit_spin.pack(side=tk.LEFT, padx=5, pady=10)
        self.canvas = tk.Canvas(self.root,  width=self.cols * self.cell_size,height=self.rows * self.cell_size, bg='white')
        self.canvas.pack(pady=10)
    
    def solve_or_reset_maze(self):
        if self.robot_pos != self.start_pos:
            self.reset_robot_to_start()
            self.solve_reset_btn.config(text="Найти выход")
        else:
            self.solve_maze_from_start()
    
    def initialize_game(self):
        self.reset_game_state()
        self.build_maze()
    
    def reset_game_state(self):
        self.maze = []
        self.robot_pos = self.start_pos
        self.exits = []
        self.path = []
        self.path_rects = []
        self.robot_circle = None
        self.found_exits = set() 
        self.solve_reset_btn.config(text="Найти выход")
    
    def reset_robot_to_start(self):
        self.robot_pos = self.start_pos
        self.path = []
        self.draw_maze()
    
    def build_maze(self):
        self.canvas.delete("all")
        self.reset_game_state()
        self.maze = [[1 for _ in range(self.cols)] for _ in range(self.rows)]
        start_x, start_y = self.start_pos
        self.maze[start_y][start_x] = 0
        stack = [(start_x, start_y)]
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        
        while stack:
            x, y = stack[-1]
            random.shuffle(directions)
            found = False
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (0 < nx < self.cols - 1 and 0 < ny < self.rows - 1 and 
                    self.maze[ny][nx] == 1):
                    wx, wy = x + dx // 2, y + dy // 2
                    self.maze[wy][wx] = 0
                    self.maze[ny][nx] = 0
                    stack.append((nx, ny))
                    found = True
                    break
            
            if not found:
                stack.pop()
        
        self.generate_exits()
        self.draw_maze()
    
    def generate_exits(self):
        required_exits = min(self.exit_count.get(), 5)
        self.exits = []
        attempts = 0
        while len(self.exits) < required_exits and attempts < 200:
            side = random.choice(['top', 'right', 'bottom', 'left'])
            if side == 'top':
                x = random.randint(1, self.cols - 2)
                y = 0
                check_y = 1
            elif side == 'right':
                x = self.cols - 1
                y = random.randint(1, self.rows - 2)
                check_x = x - 1
            elif side == 'bottom':
                x = random.randint(1, self.cols - 2)
                y = self.rows - 1
                check_y = y - 1
            else:
                x = 0
                y = random.randint(1, self.rows - 2)
                check_x = 1
            can_be_exit = False
            if side in ['top', 'bottom']:
                can_be_exit = self.maze[check_y][x] == 0
            else:
                can_be_exit = self.maze[y][check_x] == 0
            
            if can_be_exit and (x, y) not in self.exits:
                too_close = False
                for exit_x, exit_y in self.exits:
                    distance = abs(x - exit_x) + abs(y - exit_y)
                    if distance <= 1:
                        too_close = True
                        break
                
                if not too_close and (x, y) != self.start_pos:
                    self.maze[y][x] = 0
                    self.exits.append((x, y))
            attempts += 1

    def draw_maze(self):
        self.canvas.delete("all")
        self.path_rects = []
        for y in range(self.rows):
            for x in range(self.cols):
                if (x, y) in self.exits:
                    if (x, y) in self.found_exits:
                        color = self.colors['found_exit']
                    else:
                        color = self.colors['exit']
                elif (x, y) == self.start_pos:
                    color = self.colors['start']
                elif (x, y) in self.path:
                    color = self.colors['route']
                elif self.maze[y][x] == 1:
                    color = self.colors['wall']
                else:
                    color = 'white'
                rect_id = self.canvas.create_rectangle(
                    x * self.cell_size, y * self.cell_size,
                    (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                    fill=color, outline='gray'
                )
                if self.maze[y][x] == 0:
                    self.path_rects.append((x, y, rect_id))
        if self.robot_pos != self.start_pos:
            start_x, start_y = self.start_pos
            self.canvas.create_rectangle(
                start_x * self.cell_size, start_y * self.cell_size,
                (start_x + 1) * self.cell_size, (start_y + 1) * self.cell_size,
                fill=self.colors['start'], outline='gray'
            )
        self.draw_robot(self.robot_pos[0], self.robot_pos[1])
    
    def draw_robot(self, x, y):
        robot_center_x = (x + 0.5) * self.cell_size
        robot_center_y = (y + 0.5) * self.cell_size
        robot_radius = self.cell_size * self.robot_radius_ratio
        if self.robot_circle:
            self.canvas.delete(self.robot_circle)
        self.robot_circle = self.canvas.create_oval(
            robot_center_x - robot_radius, robot_center_y - robot_radius,
            robot_center_x + robot_radius, robot_center_y + robot_radius,
            fill=self.colors['robot'], outline='darkblue'
        )
    
    def solve_maze_from_start(self):
        start_x, start_y = self.start_pos
        available_exits = [exit for exit in self.exits if exit not in self.found_exits]
        if not available_exits:
            messagebox.showinfo("Результат", "Все выходы уже найдены!")
            return
        
        maze_copy = [row[:] for row in self.maze]
        self.path = []
        queue = [(start_y, start_x)]
        visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        visited[start_y][start_x] = True
        parent = {}
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        found_exit = None
        front_index = 0
        
        while front_index < len(queue):
            y, x = queue[front_index]
            front_index += 1
            if (x, y) in available_exits:
                found_exit = (y, x)
                break
            for dy, dx in directions:
                ny, nx = y + dy, x + dx
                if (0 <= ny < self.rows and 0 <= nx < self.cols and 
                    not visited[ny][nx] and maze_copy[ny][nx] == 0):
                    visited[ny][nx] = True
                    parent[(ny, nx)] = (y, x)
                    queue.append((ny, nx))
        
        if found_exit:
            current = found_exit
            while current != (start_y, start_x):
                self.path.append((current[1], current[0]))
                current = parent[current]
            self.path.append((start_x, start_y))
            self.path.reverse()
            exit_x, exit_y = self.path[-1]
            self.found_exits.add((exit_x, exit_y))
            self.robot_pos = (exit_x, exit_y)
            self.solve_reset_btn.config(text="Сбросить поиск")
            self.animate_solution()
        else:
            messagebox.showinfo("Результат", "Путь к выходу не найден!")
    
    def animate_solution(self):
        self.animate_robot_movement(0)
    
    def animate_robot_movement(self, step):
        if step < len(self.path):
            x, y = self.path[step]
            self.robot_pos = (x, y)
            if step > 0:
                prev_x, prev_y = self.path[step - 1]
                if (prev_x, prev_y) not in self.exits and (prev_x, prev_y) != self.start_pos:
                    for rect_x, rect_y, rect_id in self.path_rects:
                        if rect_x == prev_x and rect_y == prev_y:
                            self.canvas.itemconfig(rect_id, fill=self.colors['route'])
                            break
            self.draw_robot(x, y)
            delay = 70
            self.root.after(delay, lambda: self.animate_robot_movement(step + 1))
        else:
            exit_x, exit_y = self.path[-1]
            self.draw_maze()
            
            messagebox.showinfo("Успех!", f"Робот нашел выход!\n"
                              f"Найдено выходов: {len(self.found_exits)}/{len(self.exits)}")

def main():
    root = tk.Tk()
    game = MazeGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()