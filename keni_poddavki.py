import tkinter as tk
from tkinter import messagebox
import hashlib
import os
import random

BOARD_SIZE = 8
CELL_SIZE = 70
MARGIN = 50
MAX_MOVES_WITHOUT_CAPTURE = 10

COLORS = {
    'background': '#DEB887',
    'board_light': '#F5DEB3',
    'board_dark': '#D2B48C',
    'highlight': 'yellow',
    'white_ken': 'white',
    'black_ken': 'black',
    'white_outline': 'black',
    'black_outline': 'white',
    'pepper_red': 'red',
    'pepper_gold': 'gold',
}

USERS_FILE = 'users.txt'

board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
selected_ken = None
current_player = 'white'
game_over = False
moves_without_capture = 0
player_users = {'white': None, 'black': None}


root = tk.Tk()
root.title("Кены - поддавки")
root.geometry("900x700")
root.resizable(False, False)
root.configure(bg=COLORS['background'])

canvas = tk.Canvas(root, width=900, height=700, bg=COLORS['background'])

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def save_user(username, password):
    with open(USERS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username}:{hash_password(password)}\n")

def load_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) == 2:
                    users[parts[0]] = parts[1]
    return users

def register_user(login, password):
    users = load_users()
    if login in users:
        return False, "Логин уже занят"
    
    save_user(login, password)
    return True, "Успешная регистрация"

def login_user(login, password):
    users = load_users()
    if login not in users:
        return False, "Пользователь не найден"
    
    if users[login] != hash_password(password):
        return False, "Неверный пароль"
    
    return True, "Успешный вход"

def show_login():
    login_window = tk.Toplevel(root)
    login_window.title("Авторизация игроков")
    login_window.geometry("400x450")
    login_window.resizable(False, False)
    login_window.transient(root)
    login_window.grab_set()
    login_window.update_idletasks()
    x = (root.winfo_screenwidth() - 400) // 2
    y = (root.winfo_screenheight() - 450) // 2
    login_window.geometry(f"400x450+{x}+{y}")
    current_step = [1]
    content_frame = tk.Frame(login_window)
    content_frame.pack(pady=20)
    title_label = tk.Label(content_frame, text="", font=("Arial", 14, "bold"))
    title_label.pack(pady=10)
    tk.Label(content_frame, text="Логин:", font=("Arial", 11)).pack(pady=5)
    login_entry = tk.Entry(content_frame, width=30, font=("Arial", 11))
    login_entry.pack(pady=5)
    
    tk.Label(content_frame, text="Пароль:", font=("Arial", 11)).pack(pady=5)
    password_entry = tk.Entry(content_frame, width=30, show="*", font=("Arial", 11))
    password_entry.pack(pady=5)
    
    status_label = tk.Label(content_frame, text="", font=("Arial", 10))
    status_label.pack(pady=10)
    
    def update_title():
        if current_step[0] == 1:
            title_label.config(text="ИГРОК 1 (белые кены)")
        else:
            title_label.config(text="ИГРОК 2 (черные кены)")
    
    def auth_action(is_login=True):
        login = login_entry.get().strip()
        password = password_entry.get()
        
        if not login or not password:
            messagebox.showerror("Ошибка", "Введите логин и пароль")
            return
        
        if len(login) < 3 or len(password) < 3:
            messagebox.showerror("Ошибка", "Логин и пароль должны быть от 3 символов")
            return
        
        if is_login:
            success, msg = login_user(login, password)
        else:
            success, msg = register_user(login, password)
        
        if success:
            assign_player(login)
        else:
            messagebox.showerror("Ошибка", msg)
    
    def assign_player(login):
        if current_step[0] == 1:
            player_users['white'] = login
            status_label.config(text=f"Игрок 1: {login}", fg="green")
            current_step[0] = 2
            login_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
            status_label.config(text="")
            update_title()
        else:
            if login == player_users['white']:
                messagebox.showerror("Ошибка", "Этот логин уже используется")
                return
            player_users['black'] = login
            login_window.destroy()
            start_game()
    
    button_frame = tk.Frame(content_frame)
    button_frame.pack(pady=10)
    
    tk.Button(button_frame, text="Войти", 
              command=lambda: auth_action(True), font=("Arial", 11), width=12).pack(side=tk.LEFT, padx=5)
    
    tk.Button(button_frame, text="Регистрация", 
              command=lambda: auth_action(False), font=("Arial", 11), width=12).pack(side=tk.LEFT, padx=5)
    
    update_title()


def init_board():
    global board
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            board[i][j] = ''
    
    for row in [5, 6]:
        for col in range(BOARD_SIZE):
            board[row][col] = 'white_ken'
    
    for row in [1, 2]:
        for col in range(BOARD_SIZE):
            board[row][col] = 'black_ken'

def get_ken_color(ken_str):
    if not ken_str:
        return None
    parts = ken_str.split('_')
    return parts[0] if len(parts) > 0 else None

def draw_ken(row, col, ken):
    x = MARGIN + col * CELL_SIZE + CELL_SIZE//2
    y = MARGIN + row * CELL_SIZE + CELL_SIZE//2
    radius = CELL_SIZE//2 - 5
    
    ken_color = get_ken_color(ken)
    color = COLORS['white_ken'] if ken_color == 'white' else COLORS['black_ken']
    outline = COLORS['white_outline'] if ken_color == 'white' else COLORS['black_outline']
    
    canvas.create_oval(x-radius, y-radius, x+radius, y+radius,
                      fill=color, outline=outline, width=2)
    
    if 'pepper' in ken:
        fill_color = COLORS['pepper_red'] if color == 'white' else COLORS['pepper_gold']
        canvas.create_text(x, y, text="П", font=("Arial", 14, "bold"), fill=fill_color)
    else:
        fill_color = 'black' if color == 'white' else 'white'
        canvas.create_text(x, y, text="К", font=("Arial", 10, "bold"), fill=fill_color)

def draw_board():
    canvas.delete("all")
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x1 = MARGIN + col * CELL_SIZE
            y1 = MARGIN + row * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            
            color = COLORS['board_light'] if (row + col) % 2 == 0 else COLORS['board_dark']
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')
    
    for i in range(BOARD_SIZE):
        letter = chr(65 + i)
        canvas.create_text(MARGIN - 20, MARGIN + i * CELL_SIZE + CELL_SIZE//2, 
                         text=letter, font=("Arial", 12, "bold"))
        canvas.create_text(MARGIN + i * CELL_SIZE + CELL_SIZE//2, MARGIN - 20, 
                         text=str(i+1), font=("Arial", 12, "bold"))
    
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            ken = board[row][col]
            if ken:
                draw_ken(row, col, ken)
    
    if selected_ken:
        row, col = selected_ken
        x1 = MARGIN + col * CELL_SIZE
        y1 = MARGIN + row * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        canvas.create_rectangle(x1, y1, x2, y2, outline=COLORS['highlight'], width=3)

def get_possible_moves(row, col):
    ken = board[row][col]
    color = get_ken_color(ken)
    
    if not ken or color != current_player:
        return [], [], []
    
    is_pepper = 'pepper' in ken
    moves, jumps, friend_jumps = [], [], []
    if current_player == 'white':
        ken_move_dirs = [(-1, 0), (0, -1), (0, 1)]
    else:
        ken_move_dirs = [(1, 0), (0, -1), (0, 1)]
    
    move_dirs = ken_move_dirs if not is_pepper else [(-1, 0), (1, 0), (0, -1), (0, 1)]
    all_dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    def cell_state(r, c):
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
            content = board[r][c]
            if content == '':
                return 'empty'
            cell_color = get_ken_color(content)
            return 'friend' if cell_color == current_player else 'enemy'
        return None
    for dr, dc in move_dirs:
        if is_pepper:
            friend_found = False
            for dist in range(1, BOARD_SIZE):
                r, c = row + dr*dist, col + dc*dist
                state = cell_state(r, c)
                
                if state is None:
                    break
                
                if state == 'empty':
                    if not friend_found:
                        moves.append((r, c))
                elif state == 'friend':
                    if not friend_found:
                        jr, jc = r + dr, c + dc
                        if cell_state(jr, jc) == 'empty':
                            friend_jumps.append((jr, jc))
                        friend_found = True
                    else:
                        break
                elif state == 'enemy':
                    if not friend_found:
                        for jump_dist in range(dist + 1, BOARD_SIZE):
                            jr, jc = row + dr*jump_dist, col + dc*jump_dist
                            jump_state = cell_state(jr, jc)
                            
                            if jump_state is None:
                                break
                            if jump_state == 'empty':
                                jumps.append((jr, jc, (r, c)))
                            else:
                                break
                    break
        else:
            r, c = row + dr, col + dc
            state = cell_state(r, c)
            
            if state == 'empty':
                moves.append((r, c))
            elif state == 'friend':
                jr, jc = r + dr, c + dc
                if cell_state(jr, jc) == 'empty':
                    friend_jumps.append((jr, jc))
    
    if not is_pepper:
        for dr, dc in all_dirs:
            mr, mc = row + dr, col + dc
            jr, jc = row + 2*dr, col + 2*dc
            
            if (cell_state(mr, mc) == 'enemy' and 
                cell_state(jr, jc) == 'empty'):
                jumps.append((jr, jc, (mr, mc)))
    
    return moves, jumps, friend_jumps

def process_move(from_row, from_col, to_row, to_col, is_capture=False, cap_pos=None):
    global selected_ken, moves_without_capture
    board[to_row][to_col] = board[from_row][from_col]
    board[from_row][from_col] = ''
    if is_capture and cap_pos:
        cr, cc = cap_pos
        board[cr][cc] = ''
        moves_without_capture = 0
    else:
        moves_without_capture += 1

    if should_promote(to_row, to_col):
        promote_to_pepper(to_row, to_col)
    
    selected_ken = None
    complete_turn()

def on_click(event):
    global selected_ken, game_over
    
    if game_over:
        return
    
    col = (event.x - MARGIN) // CELL_SIZE
    row = (event.y - MARGIN) // CELL_SIZE
    
    if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
        return
    
    if selected_ken:
        sr, sc = selected_ken
        moves, jumps, friend_jumps = get_possible_moves(sr, sc)
        target = (row, col)
        for move_row, move_col in friend_jumps:
            if (move_row, move_col) == target:
                return process_move(sr, sc, row, col)
        
        for jump_row, jump_col, cap_pos in jumps:
            if (jump_row, jump_col) == target:
                return process_move(sr, sc, row, col, True, cap_pos)
        
        for move_row, move_col in moves:
            if (move_row, move_col) == target:
                return process_move(sr, sc, row, col)
        
        if get_ken_color(board[row][col]) == current_player:
            selected_ken = (row, col)
        else:
            selected_ken = None
    else:
        if get_ken_color(board[row][col]) == current_player:
            selected_ken = (row, col)
    
    draw_board()

def should_promote(row, col):
    ken = board[row][col]
    if 'pepper' in ken:
        return False
    
    ken_color = get_ken_color(ken)
    if ken_color == 'white' and row == 0:
        return True
    elif ken_color == 'black' and row == BOARD_SIZE - 1:
        return True
    
    return False

def promote_to_pepper(row, col):
    ken_color = get_ken_color(board[row][col])
    if ken_color == 'white':
        board[row][col] = 'white_pepper'
    else:
        board[row][col] = 'black_pepper'

def check_player_status(player):
    has_kens = False
    can_move = False
    
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if get_ken_color(board[row][col]) == player:
                has_kens = True
                moves, jumps, friend_jumps = get_possible_moves(row, col)
                if moves or jumps or friend_jumps:
                    can_move = True
                    return has_kens, can_move 
    return has_kens, can_move

def check_win(player):
    has_kens, can_move = check_player_status(player)
    return not has_kens or (has_kens and not can_move)

def complete_turn():
    global current_player, game_over, moves_without_capture
    
    if moves_without_capture >= MAX_MOVES_WITHOUT_CAPTURE:
        game_over = True
        messagebox.showinfo("Игра окончена", "Ничья! 10 ходов без взятия.")
        return
    
    current_player = 'black' if current_player == 'white' else 'white'
    if check_win(current_player):
        game_over = True
        winner = current_player
        winner_name = "Белые" if winner == 'white' else "Черные"
        winner_user = player_users[winner] or winner_name
        messagebox.showinfo("Игра окончена", f"Победили {winner_name} ({winner_user})!")
        return
    
    update_info_labels()
    draw_board()

info_label = tk.Label(root, text="", font=("Arial", 16, "bold"), bg=COLORS['background'])
moves_label = tk.Label(root, text="Ходов без взятия: 0", font=("Arial", 12), bg=COLORS['background'])
player_label = tk.Label(root, text="", font=("Arial", 12), bg=COLORS['background'], anchor="w", width=20, justify="left")

def update_info_labels():
    if current_player == 'white':
        user = player_users['white'] or "Игрок 1"
        info_label.config(text=f"Ход белых ({user})")
    else:
        user = player_users['black'] or "Игрок 2"
        info_label.config(text=f"Ход черных ({user})")
    
    moves_label.config(text=f"Ходов без взятия: {moves_without_capture}")
    
    white_user = player_users['white'] or "не назначен"
    black_user = player_users['black'] or "не назначен"
    player_label.config(text=f"Белые: {white_user}\nЧерные: {black_user}")

def reset_game():
    global selected_ken, current_player, game_over, moves_without_capture
    selected_ken = None
    current_player = random.choice(['white', 'black'])
    game_over = False
    moves_without_capture = 0
    init_board()
    update_info_labels()
    draw_board()

def start_game():
    canvas.pack()
    info_label.place(x=650, y=50)
    moves_label.place(x=650, y=90)
    player_label.place(x=650, y=130)
    
    tk.Button(root, text="Новая игра", command=reset_game, 
             font=("Arial", 12), width=15).place(x=650, y=200)
    tk.Button(root, text="Выход", command=root.quit, 
             font=("Arial", 12), width=15).place(x=650, y=250)
    
    init_board()
    update_info_labels()
    draw_board()


canvas.pack_forget()
canvas.bind("<Button-1>", on_click)
root.after(100, show_login)
root.mainloop()