# Импорт необходимых библиотек
import tkinter as tk  # Библиотека для создания графического интерфейса
from tkinter import messagebox  # Модуль для отображения всплывающих окон с сообщениями
import hashlib  # Модуль для хеширования паролей (шифрования)
import os  # Модуль для работы с операционной системой и файлами
import random  # Модуль для генерации случайных чисел

# Константы игры
BOARD_SIZE = 8  # Размер игрового поля 8x8 клеток
CELL_SIZE = 70  # Размер одной клетки в пикселях
MARGIN = 50  # Отступ от краев окна до игрового поля
MAX_MOVES_WITHOUT_CAPTURE = 10  # Максимум ходов без взятия для ничьей

# Цветовая схема игры
COLORS = {
    'background': '#DEB887',  # Цвет фона окна (светло-коричневый)
    'board_light': '#F5DEB3',  # Цвет светлых клеток доски
    'board_dark': '#D2B48C',  # Цвет темных клеток доски
    'highlight': 'yellow',  # Цвет выделения выбранной фигуры
    'white_ken': 'white',  # Цвет белых фигур
    'black_ken': 'black',  # Цвет черных фигур
    'white_outline': 'black',  # Контур белых фигур
    'black_outline': 'white',  # Контур черных фигур
    'pepper_red': 'red',  # Цвет маркера "перца" для белых
    'pepper_gold': 'gold',  # Цвет маркера "перца" для черных
}

USERS_FILE = 'users.txt'  # Имя файла для хранения данных пользователей

# Глобальные переменные состояния игры
board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]  # Игровое поле 8x8
selected_ken = None  # Координаты выбранной фигуры (row, col) или None
current_player = 'white'  # Текущий игрок (начинают белые)
game_over = False  # Флаг окончания игры
moves_without_capture = 0  # Счетчик ходов без взятия фигур
player_users = {'white': None, 'black': None}  # Словарь для имен пользователей игроков

# Создание главного окна приложения
root = tk.Tk()  # Создание экземпляра главного окна
root.title("Кены - поддавки")  # Установка заголовка окна
root.geometry("900x700")  # Установка размера окна (ширина x высота)
root.resizable(False, False)  # Запрет изменения размера окна
root.configure(bg=COLORS['background'])  # Установка цвета фона окна

# Создание холста для рисования игрового поля
canvas = tk.Canvas(root, width=900, height=700, bg=COLORS['background'])

def hash_password(password):
    # Функция хеширования пароля с использованием SHA256
    return hashlib.sha256(password.encode('utf-8')).hexdigest()  # Возвращает 64-символьный хеш

def save_user(username, password):
    # Функция сохранения пользователя в файл
    with open(USERS_FILE, "a", encoding="utf-8") as f:  # Открытие файла в режиме добавления
        f.write(f"{username}:{hash_password(password)}\n")  # Запись логина и хеша пароля

def load_users():
    # Функция загрузки пользователей из файла
    users = {}  # Создание пустого словаря
    if os.path.exists(USERS_FILE):  # Проверка существования файла
        with open(USERS_FILE, "r", encoding="utf-8") as f:  # Открытие файла для чтения
            for line in f:  # Чтение файла построчно
                parts = line.strip().split(':')  # Разделение строки по двоеточию
                if len(parts) == 2:  # Проверка корректности формата
                    users[parts[0]] = parts[1]  # Добавление в словарь (логин:хеш)
    return users  # Возврат словаря пользователей

def register_user(login, password):
    # Функция регистрации нового пользователя
    users = load_users()  # Загрузка существующих пользователей
    if login in users:  # Проверка, занят ли логин
        return False, "Логин уже занят"  # Возврат ошибки
    save_user(login, password)  # Сохранение нового пользователя
    return True, "Успешная регистрация"  # Возврат успеха

def login_user(login, password):
    # Функция входа существующего пользователя
    users = load_users()  # Загрузка пользователей
    if login not in users:  # Проверка существования пользователя
        return False, "Пользователь не найден"  # Возврат ошибки
    if users[login] != hash_password(password):  # Проверка пароля
        return False, "Неверный пароль"  # Возврат ошибки
    return True, "Успешный вход"  # Возврат успеха

def show_login():
    # Функция отображения окна авторизации игроков
    login_window = tk.Toplevel(root)  # Создание дочернего окна
    login_window.title("Авторизация игроков")  # Заголовок окна
    login_window.geometry("400x450")  # Размер окна
    login_window.resizable(False, False)  # Запрет изменения размера
    login_window.transient(root)  # Связь с родительским окном
    login_window.grab_set()  # Захват фокуса ввода
    login_window.update_idletasks()  # Обновление геометрии окна
    # Центрирование окна на экране
    x = (root.winfo_screenwidth() - 400) // 2  # Координата X центра
    y = (root.winfo_screenheight() - 450) // 2  # Координата Y центра
    login_window.geometry(f"400x450+{x}+{y}")  # Установка позиции окна
    
    current_step = [1]  # Список для хранения текущего шага (игрок 1 или 2)
    content_frame = tk.Frame(login_window)  # Создание фрейма для содержимого
    content_frame.pack(pady=20)  # Размещение фрейма с отступом
    
    title_label = tk.Label(content_frame, text="", font=("Arial", 14, "bold"))  # Заголовок
    title_label.pack(pady=10)  # Размещение заголовка
    
    # Создание поля для ввода логина
    tk.Label(content_frame, text="Логин:", font=("Arial", 11)).pack(pady=5)  # Метка
    login_entry = tk.Entry(content_frame, width=30, font=("Arial", 11))  # Поле ввода
    login_entry.pack(pady=5)  # Размещение поля
    
    # Создание поля для ввода пароля
    tk.Label(content_frame, text="Пароль:", font=("Arial", 11)).pack(pady=5)  # Метка
    password_entry = tk.Entry(content_frame, width=30, show="*", font=("Arial", 11))  # Поле ввода (скрытое)
    password_entry.pack(pady=5)  # Размещение поля
    
    status_label = tk.Label(content_frame, text="", font=("Arial", 10))  # Метка статуса
    status_label.pack(pady=10)  # Размещение метки
    
    def update_title():
        # Внутренняя функция обновления заголовка окна
        if current_step[0] == 1:  # Если текущий шаг - игрок 1
            title_label.config(text="ИГРОК 1 (белые кены)")  # Установка текста для игрока 1
        else:  # Если текущий шаг - игрок 2
            title_label.config(text="ИГРОК 2 (черные кены)")  # Установка текста для игрока 2
    
    def auth_action(is_login=True):
        # Функция выполнения действия (вход или регистрация)
        login = login_entry.get().strip()  # Получение логина (удаление пробелов)
        password = password_entry.get()  # Получение пароля
        
        if not login or not password:  # Проверка на пустые поля
            messagebox.showerror("Ошибка", "Введите логин и пароль")  # Показ ошибки
            return
        
        if len(login) < 3 or len(password) < 3:  # Проверка минимальной длины
            messagebox.showerror("Ошибка", "Логин и пароль должны быть от 3 символов")
            return
        
        if is_login:  # Если выбран вход
            success, msg = login_user(login, password)  # Попытка входа
        else:  # Если выбрана регистрация
            success, msg = register_user(login, password)  # Попытка регистрации
        
        if success:  # Если успешно
            assign_player(login)  # Назначение игрока
        else:  # Если ошибка
            messagebox.showerror("Ошибка", msg)  # Показ ошибки
    
    def assign_player(login):
        # Функция назначения пользователя игроку
        nonlocal current_step  # Объявление nonlocal для изменения внешней переменной
        if current_step[0] == 1:  # Если это первый игрок
            player_users['white'] = login  # Назначение белых игроку
            status_label.config(text=f"Игрок 1: {login}", fg="green")  # Обновление статуса
            current_step[0] = 2  # Переход ко второму игроку
            login_entry.delete(0, tk.END)  # Очистка поля логина
            password_entry.delete(0, tk.END)  # Очистка поля пароля
            status_label.config(text="")  # Очистка статуса
            update_title()  # Обновление заголовка
        else:  # Если это второй игрок
            if login == player_users['white']:  # Проверка на повторный логин
                messagebox.showerror("Ошибка", "Этот логин уже используется")
                return
            player_users['black'] = login  # Назначение черных игроку
            login_window.destroy()  # Закрытие окна авторизации
            start_game()  # Запуск игры
    
    button_frame = tk.Frame(content_frame)  # Создание фрейма для кнопок
    button_frame.pack(pady=10)  # Размещение фрейма
    
    # Создание кнопки "Войти"
    tk.Button(button_frame, text="Войти", 
              command=lambda: auth_action(True), font=("Arial", 11), width=12).pack(side=tk.LEFT, padx=5)
    
    # Создание кнопки "Регистрация"
    tk.Button(button_frame, text="Регистрация", 
              command=lambda: auth_action(False), font=("Arial", 11), width=12).pack(side=tk.LEFT, padx=5)
    
    update_title()  # Инициализация заголовка

def init_board():
    # Функция инициализации игровой доски
    global board  # Объявление глобальной переменной
    # Очистка доски
    for i in range(BOARD_SIZE):  # Цикл по строкам
        for j in range(BOARD_SIZE):  # Цикл по столбцам
            board[i][j] = ''  # Очистка клетки
    
    # Расстановка белых фигур (игрок 1)
    for row in [5, 6]:  # Строки 5 и 6 (индексация с 0)
        for col in range(BOARD_SIZE):  # Все столбцы
            board[row][col] = 'white_ken'  # Установка белой фигуры
    
    # Расстановка черных фигур (игрок 2)
    for row in [1, 2]:  # Строки 1 и 2
        for col in range(BOARD_SIZE):  # Все столбцы
            board[row][col] = 'black_ken'  # Установка черной фигуры

def get_ken_color(ken_str):
    # Функция определения цвета фигуры
    if not ken_str:  # Если строка пустая
        return None  # Возврат None
    parts = ken_str.split('_')  # Разделение строки по символу '_'
    return parts[0] if len(parts) > 0 else None  # Возврат первой части (цвета)

def draw_ken(row, col, ken):
    # Функция рисования фигуры на доске
    x = MARGIN + col * CELL_SIZE + CELL_SIZE//2  # Координата X центра клетки
    y = MARGIN + row * CELL_SIZE + CELL_SIZE//2  # Координата Y центра клетки
    radius = CELL_SIZE//2 - 5  # Радиус фигуры
    
    ken_color = get_ken_color(ken)  # Получение цвета фигуры
    color = COLORS['white_ken'] if ken_color == 'white' else COLORS['black_ken']  # Выбор цвета заливки
    outline = COLORS['white_outline'] if ken_color == 'white' else COLORS['black_outline']  # Выбор цвета контура
    
    # Рисование круга (фигуры)
    canvas.create_oval(x-radius, y-radius, x+radius, y+radius,
                      fill=color, outline=outline, width=2)
    
    # Добавление буквы на фигуру
    if 'pepper' in ken:  # Если это перец
        fill_color = COLORS['pepper_red'] if color == 'white' else COLORS['pepper_gold']  # Выбор цвета буквы
        canvas.create_text(x, y, text="P", font=("Arial", 14, "bold"), fill=fill_color)  # Буква "P"
    else:  # Если это обычный кен
        fill_color = 'black' if color == 'white' else 'white'  # Контрастный цвет буквы
        canvas.create_text(x, y, text="K", font=("Arial", 10, "bold"), fill=fill_color)  # Буква "K"

def draw_board():
    # Функция рисования всей игровой доски
    canvas.delete("all")  # Очистка холста
    
    # Рисование клеток доски
    for row in range(BOARD_SIZE):  # Цикл по строкам
        for col in range(BOARD_SIZE):  # Цикл по столбцам
            x1 = MARGIN + col * CELL_SIZE  # Левый верхний угол клетки
            y1 = MARGIN + row * CELL_SIZE  # Левый верхний угол клетки
            x2 = x1 + CELL_SIZE  # Правый нижний угол клетки
            y2 = y1 + CELL_SIZE  # Правый нижний угол клетки
            
            # Чередование цветов клеток
            color = COLORS['board_light'] if (row + col) % 2 == 0 else COLORS['board_dark']
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')  # Рисование клетки
    
    # Рисование буквенных обозначений строк
    for i in range(BOARD_SIZE):  # Цикл по строкам
        letter = chr(65 + i)  # Буква (A, B, C, ...)
        canvas.create_text(MARGIN - 20, MARGIN + i * CELL_SIZE + CELL_SIZE//2, 
                         text=letter, font=("Arial", 12, "bold"))  # Буква слева
    
    # Рисование числовых обозначений столбцов
    for i in range(BOARD_SIZE):  # Цикл по столбцам
        canvas.create_text(MARGIN + i * CELL_SIZE + CELL_SIZE//2, MARGIN - 20, 
                         text=str(i+1), font=("Arial", 12, "bold"))  # Цифра сверху
    
    # Рисование всех фигур
    for row in range(BOARD_SIZE):  # Цикл по строкам
        for col in range(BOARD_SIZE):  # Цикл по столбцам
            ken = board[row][col]  # Получение фигуры
            if ken:  # Если клетка не пустая
                draw_ken(row, col, ken)  # Рисование фигуры
    
    # Выделение выбранной фигуры
    if selected_ken:  # Если есть выбранная фигура
        row, col = selected_ken  # Получение координат
        x1 = MARGIN + col * CELL_SIZE  # Левый верхний угол
        y1 = MARGIN + row * CELL_SIZE  # Левый верхний угол
        x2 = x1 + CELL_SIZE  # Правый нижний угол
        y2 = y1 + CELL_SIZE  # Правый нижний угол
        # Рисование желтой рамки
        canvas.create_rectangle(x1, y1, x2, y2, outline=COLORS['highlight'], width=3)

def get_possible_moves(row, col):
    # Функция получения всех возможных ходов для фигуры
    ken = board[row][col]  # Получение фигуры
    color = get_ken_color(ken)  # Получение цвета фигуры
    
    if not ken or color != current_player:  # Если нет фигуры или не наш ход
        return [], [], []  # Возврат пустых списков
    
    is_pepper = 'pepper' in ken  # Проверка, является ли фигура перцем
    moves, jumps, friend_jumps = [], [], []  # Инициализация списков ходов
    
    # Направления движения для обычных кенов
    if current_player == 'white':  # Белые двигаются вверх
        ken_move_dirs = [(-1, 0), (0, -1), (0, 1)]  # Вверх, влево, вправо
    else:  # Черные двигаются вниз
        ken_move_dirs = [(1, 0), (0, -1), (0, 1)]  # Вниз, влево, вправо
    
    # Направления движения: для перца - все, для кена - только вперед
    move_dirs = ken_move_dirs if not is_pepper else [(-1, 0), (1, 0), (0, -1), (0, 1)]
    all_dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Все направления для взятия
    
    def cell_state(r, c):
        # Вложенная функция определения состояния клетки
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:  # Проверка границ
            content = board[r][c]  # Получение содержимого клетки
            if content == '':  # Если клетка пустая
                return 'empty'  # Возврат 'empty'
            cell_color = get_ken_color(content)  # Получение цвета фигуры в клетке
            return 'friend' if cell_color == current_player else 'enemy'  # Свой или враг
        return None  # Клетка вне доски
    
    # Поиск возможных ходов
    for dr, dc in move_dirs:  # Для каждого направления движения
        if is_pepper:  # Если это перец (ходит на любое расстояние)
            friend_found = False  # Флаг найденной своей фигуры
            for dist in range(1, BOARD_SIZE):  # Проверка всех расстояний
                r, c = row + dr*dist, col + dc*dist  # Координаты клетки на расстоянии dist
                state = cell_state(r, c)  # Получение состояния клетки
                
                if state is None:  # Если клетка вне доски
                    break  # Прерывание цикла
                
                if state == 'empty':  # Если клетка пустая
                    if not friend_found:  # Если еще не найдены свои фигуры
                        moves.append((r, c))  # Добавление обычного хода
                elif state == 'friend':  # Если встретили свою фигуру
                    if not friend_found:  # Если это первая своя фигура
                        jr, jc = r + dr, c + dc  # Клетка за своей фигурой
                        if cell_state(jr, jc) == 'empty':  # Если за своей фигурой пусто
                            friend_jumps.append((jr, jc))  # Добавление прыжка через своего
                        friend_found = True  # Установка флага
                    else:  # Если уже была своя фигура
                        break  # Прерывание (нельзя через несколько)
                elif state == 'enemy':  # Если встретили врага
                    if not friend_found:  # Если до этого не было своих
                        # Поиск пустых клеток за врагом для взятия
                        for jump_dist in range(dist + 1, BOARD_SIZE):
                            jr, jc = row + dr*jump_dist, col + dc*jump_dist
                            jump_state = cell_state(jr, jc)
                            
                            if jump_state is None:  # Если клетка вне доски
                                break
                            if jump_state == 'empty':  # Если пустая клетка
                                jumps.append((jr, jc, (r, c)))  # Добавление взятия
                            else:  # Если клетка занята
                                break  # Прерывание
                    break  # Прерывание при встрече врага
        else:  # Если это обычный кен (ходит на 1 клетку)
            r, c = row + dr, col + dc  # Соседняя клетка
            state = cell_state(r, c)  # Получение состояния
            
            if state == 'empty':  # Если пустая
                moves.append((r, c))  # Добавление обычного хода
            elif state == 'friend':  # Если своя фигура
                jr, jc = r + dr, c + dc  # Клетка за своей фигурой
                if cell_state(jr, jc) == 'empty':  # Если за своей фигурой пусто
                    friend_jumps.append((jr, jc))  # Добавление прыжка через своего
    
    # Для обычных кенов добавляем взятие врага (прыжок на 2 клетки)
    if not is_pepper:
        for dr, dc in all_dirs:  # Проверка всех направлений
            mr, mc = row + dr, col + dc  # Клетка с врагом
            jr, jc = row + 2*dr, col + 2*dc  # Клетка за врагом
            
            # Если рядом враг и за ним пусто
            if (cell_state(mr, mc) == 'enemy' and 
                cell_state(jr, jc) == 'empty'):
                jumps.append((jr, jc, (mr, mc)))  # Добавление взятия
    
    return moves, jumps, friend_jumps  # Возврат всех возможных ходов

def process_move(from_row, from_col, to_row, to_col, is_capture=False, cap_pos=None):
    # Функция обработки выполненного хода
    global selected_ken, moves_without_capture  # Объявление глобальных переменных
    
    # Перемещение фигуры
    board[to_row][to_col] = board[from_row][from_col]  # Копирование фигуры в новую позицию
    board[from_row][from_col] = ''  # Очистка старой позиции
    
    if is_capture and cap_pos:  # Если это взятие
        cr, cc = cap_pos  # Координаты взятой фигуры
        board[cr][cc] = ''  # Удаление взятой фигуры
        moves_without_capture = 0  # Сброс счетчика ходов без взятия
    else:  # Если не взятие
        moves_without_capture += 1  # Увеличение счетчика
    
    # Проверка на превращение в перца
    if should_promote(to_row, to_col):  # Если фигура достигла края
        promote_to_pepper(to_row, to_col)  # Превращение в перца
    
    selected_ken = None  # Сброс выбранной фигуры
    complete_turn()  # Завершение хода

def on_click(event):
    # Обработчик клика мышью по холсту
    global selected_ken, game_over  # Объявление глобальных переменных
    
    if game_over:  # Если игра окончена
        return  # Игнорирование кликов
    
    # Преобразование координат клика в координаты клетки
    col = (event.x - MARGIN) // CELL_SIZE  # Столбец
    row = (event.y - MARGIN) // CELL_SIZE  # Строка
    
    # Проверка, что клик внутри доски
    if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
        return  # Выход если клик вне доски
    
    if selected_ken:  # Если уже выбрана фигура
        sr, sc = selected_ken  # Координаты выбранной фигуры
        moves, jumps, friend_jumps = get_possible_moves(sr, sc)  # Получение возможных ходов
        target = (row, col)  # Целевая клетка
        
        # Проверка прыжка через своего
        for move_row, move_col in friend_jumps:
            if (move_row, move_col) == target:  # Если кликнули на клетку для прыжка
                return process_move(sr, sc, row, col)  # Выполнение прыжка
        
        # Проверка взятия врага
        for jump_row, jump_col, cap_pos in jumps:
            if (jump_row, jump_col) == target:  # Если кликнули на клетку для взятия
                return process_move(sr, sc, row, col, True, cap_pos)  # Выполнение взятия
        
        # Проверка обычного хода
        for move_row, move_col in moves:
            if (move_row, move_col) == target:  # Если кликнули на клетку для хода
                return process_move(sr, sc, row, col)  # Выполнение хода
        
        # Если кликнули на другую свою фигуру
        if get_ken_color(board[row][col]) == current_player:
            selected_ken = (row, col)  # Выбор новой фигуры
        else:  # Если кликнули на пустую или вражескую клетку
            selected_ken = None  # Сброс выбора
    else:  # Если ничего не выбрано
        # Если кликнули на свою фигуру
        if get_ken_color(board[row][col]) == current_player:
            selected_ken = (row, col)  # Выбор фигуры
    
    draw_board()  # Перерисовка доски

def should_promote(row, col):
    # Функция проверки необходимости превращения в перца
    ken = board[row][col]  # Получение фигуры
    if 'pepper' in ken:  # Если уже перец
        return False  # Не нужно превращение
    
    ken_color = get_ken_color(ken)  # Получение цвета фигуры
    if ken_color == 'white' and row == 0:  # Белые на первой строке (верх)
        return True  # Нужно превращение
    elif ken_color == 'black' and row == BOARD_SIZE - 1:  # Черные на последней строке (низ)
        return True  # Нужно превращение
    
    return False  # Не нужно превращение

def promote_to_pepper(row, col):
    # Функция превращения фигуры в перца
    ken_color = get_ken_color(board[row][col])  # Получение цвета фигуры
    if ken_color == 'white':  # Если белая
        board[row][col] = 'white_pepper'  # Превращение в белого перца
    else:  # Если черная
        board[row][col] = 'black_pepper'  # Превращение в черного перца

def check_player_status(player):
    # Функция проверки статуса игрока
    has_kens = False  # Есть ли фигуры
    can_move = False  # Может ли ходить
    
    for row in range(BOARD_SIZE):  # Цикл по строкам
        for col in range(BOARD_SIZE):  # Цикл по столбцам
            if get_ken_color(board[row][col]) == player:  # Если нашли фигуру игрока
                has_kens = True  # У игрока есть фигуры
                moves, jumps, friend_jumps = get_possible_moves(row, col)  # Получение возможных ходов
                if moves or jumps or friend_jumps:  # Если есть хотя бы один возможный ход
                    can_move = True  # Игрок может ходить
                    return has_kens, can_move  # Возврат результата (оптимизация)
    return has_kens, can_move  # Возврат результата

def check_win(player):
    # Функция проверки победы (на самом деле проверяет проигрыш в поддавках)
    has_kens, can_move = check_player_status(player)  # Получение статуса игрока
    # Игрок проиграл если: нет фигур ИЛИ (есть фигуры и нет ходов)
    return not has_kens or (has_kens and not can_move)

def complete_turn():
    # Функция завершения хода и перехода к следующему
    global current_player, game_over, moves_without_capture  # Объявление глобальных переменных
    
    # Проверка на ничью (10 ходов без взятия)
    if moves_without_capture >= MAX_MOVES_WITHOUT_CAPTURE:
        game_over = True  # Установка флага окончания игры
        messagebox.showinfo("Игра окончена", "Ничья! 10 ходов без взятия.")  # Сообщение о ничье
        return  # Выход из функции
    
    # Смена игрока
    current_player = 'black' if current_player == 'white' else 'white'
    
    # Проверка победы (на самом деле проверка проигрыша текущего игрока)
    if check_win(current_player):  # Если текущий игрок проиграл
        game_over = True  # Установка флага окончания игры
        winner = current_player  # Определение победителя (ТОТ, КТО ТОЛЬКО ЧТО ПОЛУЧИЛ ХОД)
        winner_name = "Белые" if winner == 'white' else "Черные"  # Имя победителя
        winner_user = player_users[winner] or winner_name  # Пользователь победителя
        # Внимание: здесь ошибка логики! В поддавках победитель - ПРОТИВНИК того, кто не может ходить
        messagebox.showinfo("Игра окончена", f"Победили {winner_name} ({winner_user})!")
        return  # Выход из функции
    
    update_info_labels()  # Обновление информационных меток
    draw_board()  # Перерисовка доски

# Создание информационных меток на главном окне
info_label = tk.Label(root, text="", font=("Arial", 16, "bold"), bg=COLORS['background'])  # Метка текущего хода
moves_label = tk.Label(root, text="Ходов без взятия: 0", font=("Arial", 12), bg=COLORS['background'])  # Метка счетчика
player_label = tk.Label(root, text="", font=("Arial", 12), bg=COLORS['background'], anchor="w", width=20, justify="left")  # Метка игроков

def update_info_labels():
    # Функция обновления информационных меток
    if current_player == 'white':  # Если ход белых
        user = player_users['white'] or "Игрок 1"  # Получение имени пользователя или значения по умолчанию
        info_label.config(text=f"Ход белых ({user})")  # Установка текста
    else:  # Если ход черных
        user = player_users['black'] or "Игрок 2"
        info_label.config(text=f"Ход черных ({user})")
    
    moves_label.config(text=f"Ходов без взятия: {moves_without_capture}")  # Обновление счетчика
    
    # Обновление информации об игроках
    white_user = player_users['white'] or "не назначен"  # Имя белого игрока
    black_user = player_users['black'] or "не назначен"  # Имя черного игрока
    player_label.config(text=f"Белые: {white_user}\nЧерные: {black_user}")  # Установка текста

def reset_game():
    # Функция сброса игры (новая игра)
    global selected_ken, current_player, game_over, moves_without_capture  # Объявление глобальных переменных
    selected_ken = None  # Сброс выбранной фигуры
    current_player = random.choice(['white', 'black'])  # Случайный выбор начинающего
    game_over = False  # Сброс флага окончания игры
    moves_without_capture = 0  # Сброс счетчика ходов без взятия
    init_board()  # Инициализация доски
    update_info_labels()  # Обновление информации
    draw_board()  # Перерисовка доски

def start_game():
    # Функция начала игры после авторизации
    canvas.pack()  # Отображение холста
    
    # Размещение информационных меток
    info_label.place(x=650, y=50)  # Метка текущего хода
    moves_label.place(x=650, y=90)  # Метка счетчика ходов без взятия
    player_label.place(x=650, y=130)  # Метка информации об игроках
    
    # Создание кнопки "Новая игра"
    tk.Button(root, text="Новая игра", command=reset_game, 
             font=("Arial", 12), width=15).place(x=650, y=200)
    
    # Создание кнопки "Выход"
    tk.Button(root, text="Выход", command=root.quit, 
             font=("Arial", 12), width=15).place(x=650, y=250)
    
    # Инициализация и запуск игры
    init_board()  # Инициализация доски
    update_info_labels()  # Обновление информации
    draw_board()  # Отрисовка доски

# Инициализация приложения
canvas.pack_forget()  # Скрытие холста до начала игры
canvas.bind("<Button-1>", on_click)  # Привязка обработчика клика мыши
root.after(100, show_login)  # Показ окна авторизации через 100 мс
root.mainloop()  # Запуск главного цикла обработки событий Tkinter