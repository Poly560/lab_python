import re
dct = {
    "0": "ноль",
    "1": "один",
    "2": "два",
    "3": "три",
    "4": "четыре",
    "5": "пять",
    "6": "шесть",
    "7": "семь",
    "8": "восемь",
    "9": "девять",
    ",": "запятая",
}


# def is_float(s):
#     try:
#         float(s)
#         return True
#     except ValueError:
#         return False


# def check(s):
#     res = s.split(".", maxsplit=1)
#     if len(res) == 1:
#         return True
#     else:
#         return len(res[1]) <= 7


def str_to_word(s):
    return " ".join(dct.get(num, num) for num in s)

is_first = True
float_pattern = re.compile(r"^-?\d+(\.\d{1,7})?$")
with open("lab2_text.txt", "r") as f:
    for line in f.readlines():
        for word in line.split():
            if float_pattern.match(word):
                word = word.replace(".", ",")
                if is_first:
                    print(str_to_word(word))
                    is_first = False
                else:
                    print(word)