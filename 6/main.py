import math

bch_table = [
    (7, 4, 3, 1),
    (15, 11, 4, 1),
    (15, 7, 8, 2),
    (15, 5, 10, 3),
    (31, 26, 5, 1),
    (31, 21, 10, 2),
    (31, 16, 15, 3),
    (31, 11, 20, 5),
    (31, 6, 25, 7),
    (63, 57, 6, 1),
    (63, 51, 13, 2),
    (63, 45, 18, 3),
    (63, 39, 24, 4),
    (63, 36, 27, 5),
    (63, 30, 33, 6),
    (63, 24, 39, 7),
    (63, 18, 35, 10),
    (63, 16, 37, 11),
    (63, 10, 53, 13),
    (63, 7, 56, 15),
    (127, 120, 7, 1),
    (127, 113, 14, 2),
    (127, 106, 21, 3),
    (127, 99, 28, 4),
    (127, 92, 35, 5),
    (127, 85, 42, 6),
    (127, 78, 49, 7),
    (127, 71, 56, 9),
    (127, 64, 63, 10),
    (127, 57, 70, 11),
    (127, 50, 77, 13),
    (127, 43, 84, 14),
    (127, 36, 91, 15),
    (127, 29, 98, 21),
    (127, 22, 105, 23),
    (127, 15, 112, 27),
    (127, 8, 119, 31),
    (255, 247, 8, 1),
    (255, 239, 16, 2),
    (255, 231, 24, 3),
    (255, 223, 32, 4),
    (255, 215, 40, 5),
    (255, 207, 48, 6),
    (255, 199, 56, 7),
]

polynomials_table = [
    [None, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [
        1,
        "111",
        "1011",
        "10011",
        "100101",
        "1000011",
        "10001001",
        "100011101",
        "1000010001",
        "10000001001",
    ],
    [
        3,
        None,
        "1101",
        "11111",
        "111101",
        "1010111",
        "10001111",
        "101110111",
        "1001011001",
        "10000001111",
    ],
    [
        5,
        None,
        None,
        "111",
        "110111",
        "1100111",
        "10011101",
        "111110011",
        "1100110001",
        "10100001101",
    ],
    [
        7,
        None,
        None,
        "11001",
        "101111",
        "1001001",
        "11110111",
        "101101001",
        "1010011001",
        "11111111001",
    ],
    [
        9,
        None,
        None,
        None,
        "110111",
        "1101",
        "10111111",
        "110111101",
        "1100010011",
        "10010101111",
    ],
    [
        11,
        None,
        None,
        None,
        "111011",
        "1101101",
        "11010101",
        "111100111",
        "1000101101",
        "10000110101",
    ],
    [
        13,
        None,
        None,
        None,
        None,
        None,
        "10000011",
        "100101011",
        "1001110111",
        "10001101111",
    ],
    [15, None, None, None, None, None, None, "111010111", "1101100001", "10110101011"],
    [17, None, None, None, None, None, None, "010011", "1011011011", "11101001101"],
    [
        19,
        None,
        None,
        None,
        None,
        None,
        "11001011",
        "101100101",
        "1110000101",
        "10111111011",
    ],
    [
        21,
        None,
        None,
        None,
        None,
        None,
        "11100101",
        "110001011",
        "1000010111",
        "11111101011",
    ],
    [23, None, None, None, None, None, None, "101100011", "1111101001", "10000011011"],
    [25, None, None, None, None, None, None, "100011011", "1111100011", "10100100011"],
    [27, None, None, None, None, None, None, "100111111", "1110001111", "11101111011"],
    [29, None, None, None, None, None, None, None, "101101011", "10100110001"],
    [31, None, None, None, None, None, None, None, None, "11000100001"],
    [33, None, None, None, None, None, None, None, None, "111101"],
    [35, None, None, None, None, None, None, None, "1100000001", "11000010011"],
    [37, None, None, None, None, None, None, "101011111", "1001101111", "11101110011"],
    [39, None, None, None, None, None, None, None, "1111001101", "10001000111"],
    [41, None, None, None, None, None, None, None, "1101110011", "10111100101"],
    [43, None, None, None, None, None, None, "111000011", "1111001011", "10100011001"],
    [45, None, None, None, None, None, None, "100111001", "1001111101", "11000110001"],
    [47, None, None, None, None, None, None, None, None, "11001111111"],
    [49, None, None, None, None, None, None, None, None, "11101010101"],
    [51, None, None, None, None, None, None, "011111", "1111010101", "10101100111"],
    [53, None, None, None, None, None, None, None, "1010010101", "10110001111"],
    [55, None, None, None, None, None, None, None, "1010111101", "11100101011"],
    [57, None, None, None, None, None, None, None, None, "11001010001"],
    [59, None, None, None, None, None, None, None, None, "11100111001"],
    [67, None, None, None, None, None, None, None, None, "10111000001"],
    [69, None, None, None, None, None, None, None, None, "11011010011"],
]


def binary_xor(a, b):
    max_len = max(len(a), len(b))
    a = a.zfill(max_len)
    b = b.zfill(max_len)
    result = "".join(str(int(x) ^ int(y)) for x, y in zip(a, b))
    return result


def binary_mod2_div(dividend, divisor):
    dividend = dividend.lstrip("0")
    divisor = divisor.lstrip("0")
    if len(divisor) == 0:
        raise ValueError("Деление на ноль")

    dividend = list(dividend)
    divisor_len = len(divisor)
    remainder = dividend[: divisor_len - 1]

    for i in range(divisor_len - 1, len(dividend)):
        current = remainder + [dividend[i]]
        current_str = "".join(current)
        if current_str[0] == "1":
            remainder = list(binary_xor(current_str, divisor))[1:]
        else:
            remainder = current[1:]

    return "".join(remainder).lstrip("0") or "0"


def binary_weight(s):
    return s.count("1")


def cyclic_shift_left(s):
    return s[1:] + s[0]


def cyclic_shift_right(s):
    return s[-1] + s[:-1]


def multiply_by_xk(seq, k):
    return seq + "0" * k


def binary_addition(a, b):
    max_len = max(len(a), len(b))
    a = a.zfill(max_len)
    b = b.zfill(max_len)
    return binary_xor(a, b)


def binary_multiply(a, b):
    """Умножение двоичных многочленов"""
    a = a.lstrip("0")
    b = b.lstrip("0")
    if a == "" or b == "":
        return "0"

    result = "0"
    for i in range(len(b)):
        if b[len(b) - 1 - i] == "1":
            shifted = a + "0" * i
            result = binary_addition(result, shifted)
    return result


def find_bch_params(k, s):
    """Поиск параметров БЧХ кода в таблице"""
    for n, k_table, r, s_table in bch_table:
        if k_table >= k and s_table >= s:
            return n, k_table, r, s_table
    return None, None, None, None


def get_polynomial_from_table(h, i):
    """Получение многочлена из таблицы по h и i"""
    if h < 2 or h > 10:
        return None

    # Находим индекс столбца для h
    h_index = polynomials_table[0].index(h)

    # Находим индекс строки для i
    i_index = None
    for row_idx, row in enumerate(polynomials_table):
        if row[0] == i:
            i_index = row_idx
            break

    if i_index is None or h_index is None:
        return None

    return polynomials_table[i_index][h_index]


# Ввод данных
a = input("Введите исходную двоичную последовательность: ").strip()
s = int(input("Введите число исправляемых ошибок s: "))

# Расчет параметров
k = len(a)
print(f"Число информационных разрядов k = {k}")

# Поиск параметров в таблице БЧХ
n, k_table, r, s_table = find_bch_params(k, s)
if n is None:
    print("Подходящие параметры БЧХ кода не найдены!")
    exit()

print(f"Найденные параметры БЧХ кода: n={n}, k={k_table}, r={r}, s={s_table}")

# Дополнение исходной последовательности до k_table
if k < k_table:
    a = "0" * (k_table - k) + a
    print(f"Исходная последовательность дополнена до {k_table} бит: {a}")

# Вычисление h
h = math.ceil(math.log2(n + 1))
print(f"h = ⌈log2({n}+1)⌉ = {h}")

# Вычисление индексов для минимальных многочленов
indices = []
for i in range(2 * s - 1, 0, -2):
    indices.append(i)
print(f"Индексы для минимальных многочленов: {indices}")

# Получение минимальных многочленов из таблицы
min_polynomials = []
for i in indices:
    poly = get_polynomial_from_table(h, i)
    if poly is None:
        print(f"Многочлен для i={i} не найден в таблице!")
        exit()
    min_polynomials.append(poly)
    print(f"P_{i} = {poly}")

# Вычисление образующего многочлена g(x) как произведения минимальных многочленов
g = min_polynomials[0]
for poly in min_polynomials[1:]:
    g = binary_multiply(g, poly)
print(f"Образующий многочлен g(x) = {g}")

# Формирование кодовой комбинации
alpha_xk = multiply_by_xk(a, r)
print(f"Умножение исходной последовательности на x^{r}: {alpha_xk}")

remainder = binary_mod2_div(alpha_xk, g)
print(f"Остаток от деления на g(x): {remainder}")

# Дополнение остатка до r бит
remainder = remainder.zfill(r)
beta = binary_addition(alpha_xk, remainder)
print(f"Кодовая комбинация Бетта: {beta}")

# Ввод ошибочной комбинации
print("\nВыберите вариант формирования ошибочной комбинации:")
print("1 - ввод позиций ошибок")
print("2 - ручной ввод Бетта'")
choice = input("Ваш выбор: ").strip()

beta_prime = ""
if choice == "1":
    positions = list(map(int, input("Введите позиции ошибок через пробел: ").split()))
    if len(positions) > s:
        print("Количество ошибок превышает корректирующую способность!")
        exit()
    if any(p >= len(beta) for p in positions):
        print("Есть позиция превышающая длину Бетта!")
        exit()
    if len(set(positions)) != len(positions):
        print("Есть повторяющиеся позиции!")
        exit()

    beta_list = list(beta)
    for pos in positions:
        beta_list[pos] = "1" if beta_list[pos] == "0" else "0"
    beta_prime = "".join(beta_list)
else:
    beta_prime = input("Введите Бетта': ").strip()
    if len(beta_prime) != len(beta):
        print("Длина Бетта' не совпадает с длиной Бетта!")
        exit()
    if binary_weight(binary_addition(beta, beta_prime)) > s:
        print("Количество ошибок превышает корректирующую способность!")
        exit()

print(f"Принятая последовательность: {beta_prime}")

# Обнаружение и исправление ошибок
print("\nПроцесс исправления ошибок:")
current = beta_prime
shifts = 0
max_shifts = n
found = False

while shifts < max_shifts:
    remainder = binary_mod2_div(current, g)
    weight = binary_weight(remainder)
    print(f"Сдвиг {shifts}: остаток {remainder}, вес {weight}")

    if weight <= s:
        found = True
        break

    current = cyclic_shift_left(current)
    shifts += 1

if not found:
    print("Ошибка: не удалось исправить ошибки в пределах корректирующей способности!")
    exit()

print(f"Исправление закончено. Количество сдвигов: {shifts}")
print(f"Кодовая последовательность после сдвигов: {current}")

# Сложение с остатком для исправления ошибок
corrected = binary_addition(current, remainder)
print(f"Кодовая последовательность + остаток: {current} + {remainder} = {corrected}")

# Обратный циклический сдвиг
for _ in range(shifts):
    corrected = cyclic_shift_right(corrected)

print(f"Исправленная последовательность: {corrected}")
