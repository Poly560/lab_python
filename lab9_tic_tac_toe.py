import tkinter as tk

root = tk.Tk()
root.title("Крестики-нолики")
root.geometry("400x500")
root.configure(bg='white')
root.resizable(False, False)

current_player = "X"
board = [""] * 9
game_over = False
game_vs_robot = False

def get_winning_move(player):
    lines = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for line in lines:
        values = [board[i] for i in line]
        if values.count(player) == 2 and values.count("") == 1:
            return line[values.index("")]
    return -1

def robot_move():
    move = get_winning_move("O")
    if move != -1:
        return move
    move = get_winning_move("X")
    if move != -1: 
        return move
    if board[4] == "": 
        return 4
    corners = [0, 2, 6, 8]
    for corner in corners:
        if board[corner] == "": 
            return corner
    sides = [1, 3, 5, 7]
    for side in sides:
        if board[side] == "": 
            return side
    return -1

def check_winner():
    lines = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for line in lines:
        if board[line[0]] == board[line[1]] == board[line[2]] != "":
            return board[line[0]]
    return None

def get_player_name(mark):
    if game_vs_robot:
        return "Игрок" if mark == "X" else "Робот"
    else:
        return "Игрок 1" if mark == "X" else "Игрок 2"

def make_move(index):
    global current_player, game_over
    if board[index] == "" and not game_over:
        board[index] = current_player
        buttons[index].config(text=current_player, state="disabled")
        winner = check_winner()
        if winner:
            game_over = True
            winner_name = get_player_name(winner)
            status_label.config(text=f"Ходит: {get_player_name(current_player)}\nИгра против {'робота' if game_vs_robot else 'другого игрока'}")
            result_label.config(text=f"Выиграл {winner_name}!")
        elif "" not in board:
            game_over = True
            status_label.config(text=f"Ходит: {get_player_name(current_player)}\nИгра против {'робота' if game_vs_robot else 'другого игрока'}")
            result_label.config(text="Ничья!")
        else:
            current_player = "O" if current_player == "X" else "X"
            update_status()
            if game_vs_robot and current_player == "O" and not game_over:
                root.after(200, make_robot_move)

def make_robot_move():
    move = robot_move()
    if move != -1:
        make_move(move)

def update_status():
    mode_text = "робота" if game_vs_robot else "другого игрока"
    current_player_name = get_player_name(current_player)
    status_label.config(text=f"Ходит: {current_player_name}\nИгра против {mode_text}")
    result_label.config(text="")

def toggle_mode():
    global game_vs_robot
    game_vs_robot = not game_vs_robot
    mode_btn.config(text="Другой игрок" if not game_vs_robot else "Робот")
    new_game()

def new_game():
    global board, current_player, game_over
    board = [""] * 9
    current_player = "X"
    game_over = False
    for button in buttons:
        button.config(text="", state="normal", bg='white')
    
    update_status()
    result_label.config(text="")

frame = tk.Frame(root, bg='black')
frame.place(relx=0.5, rely=0.4, anchor='center')
buttons = []
for i in range(9):
    btn = tk.Button(frame, text="", font=("Arial", 20, "bold"), width=4, height=2, command=lambda idx=i: make_move(idx), bg='white', relief='solid', bd=2)
    btn.grid(row=i//3, column=i%3, padx=1, pady=1) 
    buttons.append(btn)

status_label = tk.Label(root, text="", font=("Arial", 12), bg='white', justify='center')
status_label.place(relx=0.5, rely=0.75, anchor='center')
result_label = tk.Label(root, text="", font=("Arial", 14, "bold"), bg='white', justify='center', fg='#D43F3A')
result_label.place(relx=0.5, rely=0.82, anchor='center')
mode_btn = tk.Button(root, text="Другой игрок", font=("Arial", 12), command=toggle_mode, bg='white', relief='solid', bd=1)
mode_btn.place(relx=0.3, rely=0.9, anchor='center')
new_game_btn = tk.Button(root, text="Новая игра", font=("Arial", 12), command=new_game, bg='white', relief='solid', bd=1)
new_game_btn.place(relx=0.7, rely=0.9, anchor='center')
new_game()
root.mainloop()