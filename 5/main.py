import math


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


# Основная программа
polynomials = [
    "11",
    "101",
    "111",
    "1001",
    "1011",
    "1101",
    "1111",
    "10001",
    "10011",
    "10101",
    "10111",
    "11001",
    "11011",
    "11101",
    "11111",
    "100001",
    "100011",
    "100101",
    "100111",
    "101001",
    "101011",
    "101101",
    "101111",
    "110001",
    "110101",
    "110111",
]

# Ввод данных
a = input("Введите исходную двоичную последовательность: ").strip()
t = int(input("Введите корректирующую способность t: "))

# Расчет параметров
k = len(a)
print(f"Число информационных разрядов k = {k}")

r = math.ceil(math.log2(k + 1 + math.ceil(math.log2(k + 1))))
print(f"r = ⌈log2({k} + 1 + ⌈log2({k} + 1)⌉)⌉ = {r}")

n = k + r
print(f"n = k + r = {k} + {r} = {n}")

d0 = 2 * t + 1
print(f"d0 = 2t + 1 = 2*{t} + 1 = {d0}")

# Выбор образующего многочлена
polynomials1 = [p for p in polynomials if len(p) - 1 >= r]
print("\nУсловие 1: длина многочлена >= r")
print("Многочлены1:", polynomials1)

polynomials2 = [p for p in polynomials1 if binary_weight(p) >= d0]
print("\nУсловие 2: число ненулевых разрядов >= d0")
print("Многочлены2:", polynomials2)

check_poly = "1" + "0" * (n - 1) + "1"
print(f"\nПроверочный многочлен: x^{n} + 1 = {check_poly}")

g = None
for poly in polynomials2:
    remainder = binary_mod2_div(check_poly, poly)
    if remainder == "0":
        g = poly
        break

if g is None:
    print("Подходящий образующий многочлен не найден!")
    exit()

print(f"Образующий многочлен g(x) = {g}")

# Формирование кодовой комбинации
alpha_xk = multiply_by_xk(a, r)
print(f"\nУмножение исходной последовательности на x^{r}: {alpha_xk}")

remainder = binary_mod2_div(alpha_xk, g)
print(f"Остаток от деления на g(x): {remainder}")

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
    if len(positions) > t:
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
    if binary_weight(binary_addition(beta, beta_prime)) > t:
        print("Количество ошибок превышает корректирующую способность!")
        exit()

print(f"Принятая последовательность: {beta_prime}")

# Обнаружение и исправление ошибок
print("\nПроцесс исправления ошибок:")
current = beta_prime
shifts = 0
while True:
    remainder = binary_mod2_div(current, g)
    weight = binary_weight(remainder)
    print(f"Сдвиг {shifts}: остаток {remainder}, вес {weight}")

    if weight <= t:
        break

    current = cyclic_shift_left(current)
    shifts += 1
print(
    f"Исправление законченно. Количество сдвигов: {shifts}, кодовая последовательность: {current}"
)

corrected = binary_addition(current, remainder)
print(f"Кодовая последовательность + остаток: {current} + {remainder} = {corrected}")
for _ in range(shifts):
    corrected = cyclic_shift_right(corrected)

print(f"Исправленная последовательность: {corrected}")
