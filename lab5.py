from time import time
from itertools import product
fruits = ["ф1", "ф2", "ф3", "ф4", "ф5", "ф6", "ф7", "ф8", "ф9", "ф10"]
days = 7
# Способ №1 Алгоритмический
# def keep_all_menus(fruits, days):
#     all_menus = [[]]
#     for _ in range(days):
#         new_menus = []
#         for menu in all_menus:
#             for fruit in fruits:
#                 new_menus.append(menu + [fruit])
#         all_menus = new_menus
#     return all_menus
# start_time = time()
# all_menus = keep_all_menus(fruits, days)
# end_time = time()
# algorithmic_time = end_time - start_time
# print(f"Количество вариантов меню (алгоритмический): {len(all_menus)}")
# print(f"Время выполнения (алгоритмический): {algorithmic_time:.6f} секунд")
# for i in range(1000):
#     print(all_menus[i])
# # Способ №2 Используя itertools
# start_time = time()
# all_menus = list(product(fruits, repeat=days))
# end_time = time()
# itertools_time = end_time - start_time
# print(f"Количество вариантов меню (itertools): {len(all_menus)}")
# print(f"Время выполнения (itertools): {itertools_time:.6f} секунд")
# # # for i in range(1000):
# # #     print(all_menus[i])
# Способ №3 Рекурсивный, с добавлением условия: в последние 2 дня ребенок ест только ф2 и необходимо найти самое дешевое меню
def keep_all_menus(fruits, days):
    all_menus=[]
    def create_a_menu(menu, day):
        if day==days:
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

start_time = time()
all_menus=keep_all_menus(fruits, days)
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

# Целевая функция - вычисляет суммарную стоимость меню и находит наиболее дешевое меню
def target_function(menu, prices):
    return sum(prices[fruit] for fruit in menu)
min_cost = 10**10
best_menu = None
for menu in all_menus:
    cost = target_function(menu, prices)
    if cost < min_cost:
        min_cost = cost
        best_menu = menu

print("Самое бюджетное меню:", best_menu)
print("Минимальная стоимость:", min_cost)
end_time = time()
recursiev_time = end_time - start_time
print(f"Количество вариантов меню (рекурсивный): {len(all_menus)}")
print(f"Время выполнения (рекурсивный): {recursiev_time:.6f} секунд")

# for i in range(1000):
#     print(all_menus[i])