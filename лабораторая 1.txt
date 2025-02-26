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


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def check(s):
    res = s.split(".", maxsplit=1)
    if len(res) == 1:
        return True
    else:
        return len(res[1]) <= 7


def str_to_word(s):
    return " ".join(dct.get(num, num) for num in s)
    # lst = []
    # for num in s:
    #     symbol = dct.get(num, num)
    #     lst.append(symbol)
    # " ".join(lst)


is_first = True

with open("text.txt", "r") as f:
    for line in f.readlines():
        for word in line.split():
            if is_float(word) and check(word):
                word = word.replace(".", ",")
                if is_first:
                    print(str_to_word(word))
                    is_first = False
                else:
                    print(word)
