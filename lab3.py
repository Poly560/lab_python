# from random import randint

k, n = int(input("Введите K: ")), int(input("Введите размер матрицы: "))
middle = n // 2 + n % 2


def print_matrix(m, name):  # Вывод матрицы
    print(f"\n{name}:")
    for strk in m:
        print(" ".join(f"{elem:5}" for elem in strk))


def matrix_addition(a, f):  # Сложение матриц
    fa = [[a[i][j] + f[i][j] for j in range(n)] for i in range(n)]
    return fa


def matrix_subtraction(fa, kf):  # Вычитание матриц
    fa_kf = [[fa[i][j] - kf[i][j] for j in range(n)] for i in range(n)]
    return fa_kf


def matrix_multiplication_by_a_number(k, f):  # Умножение матрицы на число
    kf = [[k * f[i][j] for j in range(n)] for i in range(n)]
    return kf


def matrix_multiplication(a, b):  # Умножение матриц
    if len(a[0])!=len(b):
        return 0
    res=[[0 for _ in range(len(b[0]))] for _ in range(len(a))]
    for i in range(len(a[0])):
        for j in range(len(b[0])):
            for k in range(len(b)):
                res[i][j]+=a[i][k]*b[k][j]
    return res


def matrix_transposition(a):  # Транспонирование матрицы
    tr_a = [[a[j][i] for j in range(n)] for i in range(n)]
    return tr_a


# a=[[randint(-10, 10) for i in range(n)] for j in range(n)]
a = [
    [0, 2, 3, 4, 5, 0],
    [-6, 0, 8, 9, 0, 7],
    [11, 12, 0, 0, 15, 8],
    [-16, 17, 0, 0, 20, 9],
    [21, 0, 23, 24, 0, 10],
    [0, 27, 28, 29, 30, 0],
]
# a=[
#     [0, 2, 2, 2, 0],
#     [1, 0, 2, 0, 3],
#     [1, 1, 0, 3, 3],
#     [1, 0, 4, 0, 3],
#     [0, 4, 4, 4, 0]
# ]
# a=[
#     [0, 2, 2, 2, 2, 0],
#     [1, 0, 2, 2, 0, 3],
#     [1, 1, 0, 0, 3, 3],
#     [1, 1, 0, 0, 3, 3],
#     [1, 0, 4, 4, 0, 3],
#     [0, 4, 4, 4, 4, 0]
# ]
print_matrix(a, "Матрица A")
f = [r[:] for r in a]
counter_zero = 0
counter_negative = 0
# four_chank = []
# one_chank = []
for i in range(middle, n):
    for j in range(n - i, i):
        # four_chank.append(a[i][j])
        if j % 2 == 0 and a[i][j] == 0:
            counter_zero += 1

for i in range(1, n - 1):
    if i % 2 != 0:
        for j in range(i):
            if i + j < n - 1 and a[i][j] < 0:
                # one_chank.append(a[i][j])
                counter_negative += 1

# print(f'{four_chank=}, {one_chank=}')
print(counter_zero, counter_negative)
if counter_zero > counter_negative:
    for i in range(middle, n):
        for j in range(n - i, i):
            f[i][j], f[j][i] = a[j][i], a[i][j]
else:
    for i in range(1, n - 1):
        for j in range(i):
            if i + j < n - 1:
                f[i][j], f[j][i] = a[j][n - 1 - i], a[n - 1 - i][j]
print_matrix(f, "Измененная матрица F")
fa = matrix_addition(a, f)
print_matrix(fa, "Матрица F + A")
kf = matrix_multiplication_by_a_number(k, f)
print_matrix(kf, "Матрица K * F")
fa_kf = matrix_subtraction(fa, kf)
print_matrix(fa_kf, "Матрица (F + A ) – (K * F)")
tr_a = matrix_transposition(a)
print_matrix(tr_a, "Транспонированная матрица A")
result = matrix_multiplication(fa_kf, tr_a)
print_matrix(result, "Результат: матрица ((F + A) – (K * F) ) * A^T")