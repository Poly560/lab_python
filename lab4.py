import numpy as np
import matplotlib.pyplot as plt
k, n = int(input("Введите K: ")), int(input("Введите N: "))
#Определитель больше
# a = np.array([
#     [3, 3, 9, 5, 9, 2],
#     [2, 6, 5, 5, 10, 8],
#     [7, 4, 4, 8, 6, 6],
#     [6, 8, 10, 9, 8, 3],
#     [1, 1, 8, 2, 7, 5],
#     [4, 10, 10, 9, 7, 9]
# ])
#Определитель меньше
a=np.array([
    [6, 10, 5, 5, 7, 5],
    [5, 4, 5, 5, 9, 5],
    [4, 8, 6, 6, 1, 2],
    [6, 10, 4, 1, 6, 1],
    [2, 3, 5, 3, 1, 4],
    [3, 1, 8, 6, 10, 1]]
)
print("\nМатрица A:\n", a)
middle = n // 2 
b = a[:middle, :middle]
c = a[:middle, middle:]
d = a[middle:, :middle]
e = a[middle:, middle:]
f = a.copy()
count_negative = np.sum(c[:, ::2]<0)
print(f'Количество отрицательных элементов в нечетных столбцах области "C" = {count_negative}')
count_positive = np.sum(c[:, 1::2]>0)
print(f'Количество положительных элементов в четных столбцах области "C" = {count_positive}')
if count_positive > count_negative:
    # Симметричная замена B и C
    f[:middle, middle:] = np.flip(b, axis=1)
    f[:middle, :middle] = np.flip(c, axis=1)
    print("\nМатрица F после симметричной замены C и B:\n", f)
else:
    f[:middle, middle:] = np.flip(e)
    f[middle:, middle:] = np.flip(c)
    print("\nМатрица F после несимметричной замены C и E:\n", f)
det_A = np.linalg.det(a)
sum_of_diag_F = np.sum(np.diagonal(f)) + np.sum(np.fliplr(f).diagonal())
print(f"\nОпределитель A: {det_A:.2f}")
print(f"Сумма диагоналей F: {sum_of_diag_F:.2f}")
if det_A!=0:
    if det_A>sum_of_diag_F:
        inv_F=np.linalg.inv(f)
        res=a @ (a.T)- k*inv_F
        print("\nРезультат: A*A^T – K * F^-1\n", res)
    else:
        g = np.tril(a)
        inv_F=np.linalg.inv(f)
        inv_A=np.linalg.inv(a)
        res = (inv_A + g - inv_F) * k
        print("\nРезультат: (A^-1 + G - F^-1) * K\n", res)
else:
    print("Исходная матрица не верна")

#График 1
plt.figure(figsize=(10, 5))
plt.imshow(f, cmap='inferno')
plt.colorbar()
# График 2
plt.figure(figsize=(10, 5))
plt.hist(f.flatten(), bins=15, color='coral', edgecolor='black')
# График 3:
plt.figure(figsize=(7, 5))
plt.contourf(f, cmap="Spectral")
plt.colorbar()

plt.tight_layout()
plt.show()