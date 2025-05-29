import time  # 66 строк
from functools import lru_cache
def fact(n):
    factorial2 = 1
    for i in range(2, n + 1):
        factorial2 *= i
    return factorial2

@lru_cache
def f1_rec(n):
    if n == 0:
        res = 1
    elif n == 1:
        res = 2
    else:
        a = f1_rec(n - 1) / fact(n)
        b = 2 * f1_rec(n - 2) / fact(2 * n)
        c = a - b
        res = -c if n % 2 == 1 else c
    return res

def f2_iter(n):
    if n == 0:
        return 1
    elif n == 1:
        return 2
    prev2 = 1  
    prev1 = 2
    for i in range(2, n + 1):
        a = prev1 / fact(i)
        b = 2 * prev2 / fact(2 * i)
        c = a - b
        res = -c if i % 2 == 1 else c
        prev2, prev1 = prev1, res
    return res


def measure_time(func, n):
    start = time.perf_counter()
    try:
        result = func(n)
        elapsed = time.perf_counter() - start
        elapsed_ms = elapsed * 1000
        return result, elapsed_ms
    except RecursionError:
        return None, None


print(
    f"{'n':>5} | {'Рекурсивное время (мс)':>25} | {'Итеративное время (мс)':>25} | {'Рекурсивный результат':>25} | {'Итеративный результат':>25}"
)
print("-" * 130)
test_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 40, 50, 60, 70, 80, 85]
for n in test_values:
    res_rec, time_rec = measure_time(f1_rec, n)
    res_it, time_it = measure_time(f2_iter, n)

    rec_time_str = f"{time_rec:.9f}" if time_rec is not None else "Ошибка рекурсии"
    it_time_str = f"{time_it:.9f}" if time_it is not None else "Ошибка"

    rec_res_str = f"{res_rec:.6e}" if res_rec is not None else "Ошибка"
    it_res_str = f"{res_it:.6e}" if res_it is not None else "Ошибка"

    print(
        f"{n:5} | {rec_time_str:>25} | {it_time_str:>25} | {rec_res_str:>25} | {it_res_str:>25}"
    )
