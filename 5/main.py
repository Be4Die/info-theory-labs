import math
import sys

# Таблица образующих многочленов
POLYNOMIAL_TABLE = {
    1: ["11"],
    2: ["101", "111"],
    3: ["1001", "1011", "1101", "1111"],
    4: ["10001", "10011", "10101", "10111", "11001", "11011", "11101", "11111"],
    5: [
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
        "111001",
        "111011",
        "111101",
        "111111",
    ],
    6: [
        "1000001",
        "1000011",
        "1000101",
        "1000111",
        "1001001",
        "1001011",
        "1001101",
        "1001111",
        "1010001",
        "1010011",
        "1010101",
        "1010111",
        "1011001",
        "1011011",
        "1011101",
        "1011111",
        "1100001",
        "1100011",
        "1100101",
        "1100111",
        "1101001",
        "1101011",
        "1101101",
        "1101111",
        "1110001",
        "1110011",
        "1110101",
        "1110111",
        "1111001",
        "1111011",
        "1111101",
        "1111111",
    ],
    7: ["10000001", "11100001"],
    8: ["100000001", "100000011"],
    9: ["1000000001", "1100000001"],
    10: ["10000000001", "10100110111"],
    11: ["100000000001", "100000000011", "100000000101"],
    12: ["1000000000001"],
    13: ["10000000000001", "11111101111011", "11111110111011"],
    14: [
        "100000000000011",
        "100000000000101",
        "100000000000111",
        "100000000001001",
        "111111011111011",
    ],
}


def multiply_by_xr(polynomial, r):
    """Умножение полинома на x^r (сдвиг влево)"""
    return polynomial + "0" * r


def polynomial_division(dividend, divisor):
    """Деление полиномов"""
    remainder = dividend
    divisor_length = len(divisor)

    while len(remainder) >= divisor_length and "1" in remainder:
        if remainder[0] == "1":
            temp = ""
            for i in range(divisor_length):
                temp += "0" if remainder[i] == divisor[i] else "1"
            remainder = temp + remainder[divisor_length:]
        else:
            remainder = remainder[1:]

        while remainder and remainder[0] == "0":
            remainder = remainder[1:]

    return remainder.rjust(divisor_length - 1, "0")


def calculate_weight(polynomial):
    """Вычисление веса (количество единиц)"""
    return polynomial.count("1")


def cyclic_shift_left(polynomial):
    """Циклический сдвиг влево"""
    return polynomial[1:] + polynomial[0]


def cyclic_shift_right(polynomial):
    """Циклический сдвиг вправо"""
    return polynomial[-1] + polynomial[:-1]


def polynomial_addition(poly1, poly2):
    """Сложение полиномов (XOR)"""
    max_length = max(len(poly1), len(poly2))
    poly1 = poly1.rjust(max_length, "0")
    poly2 = poly2.rjust(max_length, "0")

    result = ""
    for i in range(max_length):
        result += "0" if poly1[i] == poly2[i] else "1"
    return result


def polynomial_to_string(binary_poly):
    """Красивое отображение полинома"""
    if not binary_poly:
        return "0"

    terms = []
    for i in range(len(binary_poly)):
        if binary_poly[i] == "1":
            power = len(binary_poly) - 1 - i
            if power == 0:
                terms.append("1")
            elif power == 1:
                terms.append("x")
            else:
                terms.append(f"x^{power}")

    return " + ".join(terms)


def calculate_redundancy_bits(k):
    """Вычисление количества избыточных битов"""
    r = 1
    while math.pow(2, r) < k + r + 1:
        r += 1
    return r


def generate_fallback_polynomial(r):
    """Генерация резервного многочлена"""
    return "1" + "0" * (r - 2) + "11"


def show_initial_info(original_combination):
    """Вывод начальной информации о корректирующей способности и расчетах"""
    print("\n" + "=" * 60)
    print("ИНФОРМАЦИЯ О ИСХОДНОЙ ПОСЛЕДОВАТЕЛЬНОСТИ")
    print("=" * 60)

    k = len(original_combination)

    # Корректирующая способность t = 1 (для одиночных ошибок)
    t = 1
    print(f"Корректирующая способность t = {t}")
    print(f"Число информационных разрядов k = {k}")

    # Расчет минимального кодового расстояния
    d0 = 2 * t + 1
    print(f"Минимальное кодовое расстояние d0 = 2*t + 1 = 2*{t} + 1 = {d0}")

    # Расчет r по формуле из замечания: r = ⌈log2(k + 1 + ⌈log2(k + 1)⌉)⌉
    log2_k_plus_1 = math.ceil(math.log2(k + 1))
    r_calculated = math.ceil(math.log2(k + 1 + log2_k_plus_1))
    print(f"\nРасчет минимального r по формуле:")
    print(f"  ⌈log2({k} + 1)⌉ = ⌈log2({k + 1})⌉ = {log2_k_plus_1}")
    print(
        f"  r = ⌈log2({k} + 1 + {log2_k_plus_1})⌉ = ⌈log2({k + 1 + log2_k_plus_1})⌉ = {r_calculated}"
    )

    # Расчет r по неравенству Хэмминга
    # r_hamming = calculate_redundancy_bits(k)
    # print(f"\nРасчет r по неравенству Хэмминга (2^r >= k + r + 1):")
    # print(
    #    f"  r = {r_hamming} (т.к. 2^{r_hamming} = {2**r_hamming} >= {k} + {r_hamming} + 1 = {k + r_hamming + 1})"
    # )

    print(
        f"\nМинимальная длина кодового слова n_min = k + r = {k} + {r_calculated} = {k + r_calculated}"
    )
    print(
        "Фактические значения r и n могут быть больше из-за требований к образующему полиному"
    )


def select_generator_polynomial(k, r, n, verbose=False):
    """Выбор образующего многочлена"""
    steps = [] if verbose else None

    if verbose:
        steps.append(f"k = {k}")
        steps.append(f"r = {r}")
        steps.append(f"n = {n}")
        steps.append("Выбор g(x):")
        steps.append("")

    found_suitable = False
    suitable_polynomial = ""
    current_r = r
    max_r = max(POLYNOMIAL_TABLE.keys())

    while current_r <= max_r and not found_suitable:
        if verbose:
            steps.append(f"Проверяем многочлены степени {current_r}")

        if current_r in POLYNOMIAL_TABLE:
            polynomials = POLYNOMIAL_TABLE[current_r]

            if verbose:
                steps.append(
                    f"Найдено {len(polynomials)} многочленов степени {current_r} для проверки:"
                )
                steps.append("")

            for polynomial in polynomials:
                if verbose:
                    steps.append(f"Проверяем многочлен: {polynomial}")

                polynomial_degree = len(polynomial) - 1

                # Условие 1: Степень многочлена должна быть не менее r
                condition1_str = f"Условие 1: Степень {polynomial_degree} >= r={r}: "
                if polynomial_degree < r:
                    if verbose:
                        condition1_str += "Не выполнено"
                        steps.append(condition1_str)
                        steps.append("")
                    continue
                else:
                    if verbose:
                        condition1_str += "Выполнено"
                        steps.append(condition1_str)

                # Условие 2: Число ненулевых разрядов >= 3
                non_zero_bits = calculate_weight(polynomial)
                condition2_str = (
                    f"Условие 2: Число ненулевых разрядов {non_zero_bits} >= 3: "
                )
                if non_zero_bits < 3:
                    if verbose:
                        condition2_str += "Не выполнено"
                        steps.append(condition2_str)
                        steps.append("")
                    continue
                else:
                    if verbose:
                        condition2_str += "Выполнено"
                        steps.append(condition2_str)

                # Условие 3: (x^n + 1) должно делиться на многочлен без остатка
                current_n = k + current_r
                xn_plus_1 = "1" + "0" * (current_n - 1) + "1"

                if verbose:
                    steps.append(
                        f"Условие 3: (x^{current_n} + 1) делится на g(x) без остатка:"
                    )
                    steps.append(f"  (x^{current_n} + 1) = {xn_plus_1}")
                    steps.append(f"  {xn_plus_1} / {polynomial}")

                remainder = polynomial_division(xn_plus_1, polynomial)

                if verbose:
                    steps.append(f"  Остаток: {remainder}")

                if remainder == "0" * len(remainder):
                    if verbose:
                        steps.append("  Выполнено")
                        steps.append("  g(x) подходит (выполнены все условия)")
                        steps.append("")

                    found_suitable = True
                    suitable_polynomial = polynomial
                    n = current_n
                    r = current_r
                    break
                else:
                    if verbose:
                        steps.append("  Не выполнено")
                        steps.append("")
        else:
            if verbose:
                steps.append(f"Нет многочленов степени {current_r} в таблице")
                steps.append("")

        if not found_suitable:
            if verbose:
                steps.append(f"Не найдено подходящего g(x) степени {current_r}")
                steps.append("")
            current_r += 1

    if not found_suitable:
        suitable_polynomial = generate_fallback_polynomial(r)
        if verbose:
            steps.append("Не найден подходящий многочлен среди всех степеней.")
            steps.append(f"Используется резервный многочлен: {suitable_polynomial}")
    elif verbose:
        steps.append(f"Получились: k = {k}, r = {r}, n = {n}")

    if verbose:
        steps_text = "\n".join(steps)
        return suitable_polynomial, n, steps_text
    else:
        return suitable_polynomial, n


def encode_combination(original_combination):
    """Кодирование комбинации"""
    print("\n" + "=" * 60)
    print("КОДИРОВАНИЕ КОМБИНАЦИИ")
    print("=" * 60)

    k = len(original_combination)
    r = calculate_redundancy_bits(k)
    n = k + r

    # Выбор образующего многочлена
    selected_polynomial, n = select_generator_polynomial(k, r, n)
    print(f"Исходная комбинация: {original_combination}")
    print(f"Длина информационных битов: k = {k}")
    print(f"Фактическое количество проверочных битов: r = {n - k}")
    print(f"Длина кодового слова: n = k + r = {k} + {n - k} = {n}")
    print(f"Выбранный образующий многочлен: {selected_polynomial}")
    print(f"Полиномиальная форма: {polynomial_to_string(selected_polynomial)}")

    # Кодирование
    final_r = n - k
    multiplied = multiply_by_xr(original_combination, final_r)
    print(f"\n1. Умножение {original_combination} на x^{final_r} = {multiplied}")

    remainder = polynomial_division(multiplied, selected_polynomial)
    print(f"2. Делим {multiplied} на {selected_polynomial}")
    print(f"   Остаток от деления: {remainder}")

    temp_result = multiplied[: len(multiplied) - len(remainder)]
    encoded_combination = temp_result + polynomial_addition(
        multiplied[len(multiplied) - len(remainder) :], remainder
    )
    print(f"3. Складываем {multiplied} с {remainder}")
    print(f"   Закодированная комбинация: {encoded_combination}")

    return encoded_combination, selected_polynomial, n


def introduce_error(encoded_combination, error_position):
    """Внесение ошибки в закодированную комбинацию"""
    actual_position = error_position - 1
    erroneous = list(encoded_combination)
    erroneous[actual_position] = "1" if erroneous[actual_position] == "0" else "0"
    erroneous_combination = "".join(erroneous)

    print(f"\nВнесена ошибка в позицию {error_position}")
    print(f"Ошибочная комбинация: {erroneous_combination}")

    return erroneous_combination


def decode_and_correct(erroneous_combination, generator_polynomial, original_encoded):
    """Декодирование и исправление ошибки"""
    print("\n" + "=" * 60)
    print("ОБНАРУЖЕНИЕ И ИСПРАВЛЕНИЕ ОШИБКИ")
    print("=" * 60)

    remainder = polynomial_division(erroneous_combination, generator_polynomial)
    weight = calculate_weight(remainder)

    print(f"1. Деление на {generator_polynomial}")
    print(f"   Остаток: {remainder}")
    print(f"   Вес остатка: {weight}")

    if weight == 0:
        print("   Вывод: Ошибок нет")
        return erroneous_combination

    print("   Вывод: Ошибка есть")

    current_combination = erroneous_combination
    shifts = 0

    print(f"\n2. Поиск и исправление ошибки:")

    while shifts < len(current_combination):
        rem = polynomial_division(current_combination, generator_polynomial)
        w = calculate_weight(rem)

        if shifts == 0:
            print(f"\n   Исходная комбинация: {current_combination}")
        else:
            print(f"\n   Сдвиг {shifts}: Комбинация: {current_combination}")
        print(f"   Остаток: {rem}, Вес: {w}")

        if w <= 1:
            print(f"   Вес остатка <= 1. Исправляем ошибку")

            corrected = polynomial_addition(
                current_combination, rem.rjust(len(current_combination), "0")
            )
            print(f"   После сложения с остатком: {corrected}")

            for i in range(shifts):
                corrected = cyclic_shift_right(corrected)
            print(f"   После {shifts} сдвигов вправо: {corrected}")

            print(f"\n   Исправленная комбинация: {corrected}")
            print(f"   Исходная закодированная комбинация: {original_encoded}")

            if corrected == original_encoded:
                print("   ✓ Ошибка успешно исправлена")
            else:
                print("   ⚠ Комбинация исправлена, но не совпадает с исходной")

            return corrected
        else:
            print(f"   Вес остатка > 1. Сдвиг влево")
            current_combination = cyclic_shift_left(current_combination)
            shifts += 1

    print(f"\n   Не удалось исправить ошибку после всех сдвигов")
    return erroneous_combination


def generate_all_combinations(length):
    """Генерация всех комбинаций заданной длины"""
    combinations = []
    total = int(math.pow(2, length))

    for i in range(total):
        binary = bin(i)[2:].rjust(length, "0")
        combinations.append(binary)

    return combinations


def select_generator_polynomial_for_file(k, r, n):
    """Выбор образующего многочлена (для генерации файлов)"""
    found_suitable = False
    suitable_polynomial = ""
    current_r = r
    max_r = max(POLYNOMIAL_TABLE.keys())

    while current_r <= max_r and not found_suitable:
        if current_r in POLYNOMIAL_TABLE:
            polynomials = POLYNOMIAL_TABLE[current_r]

            for polynomial in polynomials:
                polynomial_degree = len(polynomial) - 1
                if polynomial_degree < r:
                    continue

                non_zero_bits = calculate_weight(polynomial)
                if non_zero_bits < 3:
                    continue

                current_n = k + current_r
                xn_plus_1 = "1" + "0" * (current_n - 1) + "1"
                remainder = polynomial_division(xn_plus_1, polynomial)

                if remainder == "0" * len(remainder):
                    found_suitable = True
                    suitable_polynomial = polynomial
                    n = current_n
                    break

        if not found_suitable:
            current_r += 1

    if not found_suitable:
        suitable_polynomial = generate_fallback_polynomial(r)

    return suitable_polynomial, n


def encode_for_file(original_combination, generator_polynomial, r):
    """Кодирование (для генерации файлов)"""
    multiplied = multiply_by_xr(original_combination, r)
    remainder = polynomial_division(multiplied, generator_polynomial)

    temp_result = multiplied[: len(multiplied) - len(remainder)]
    encoded_combination = temp_result + polynomial_addition(
        multiplied[len(multiplied) - len(remainder) :], remainder
    )

    return encoded_combination


def generate_gx_file():
    """Генерация файла gx.txt"""
    print("Генерация файла gx.txt...")
    try:
        with open("gx.txt", "w") as file:
            for length in range(1, 11):
                combinations = generate_all_combinations(length)

                for combination in combinations:
                    k = len(combination)
                    r = calculate_redundancy_bits(k)
                    n = k + r

                    gx, n = select_generator_polynomial_for_file(k, r, n)
                    file.write(f"{combination} {gx}\n")

        print("✓ Файл gx.txt успешно создан!")
    except Exception as e:
        print(f"✗ Ошибка при создании файла gx.txt: {e}")


def generate_b_file():
    """Генерация файла b.txt"""
    print("Генерация файла b.txt...")
    try:
        with open("b.txt", "w") as file:
            for length in range(1, 11):
                combinations = generate_all_combinations(length)

                for combination in combinations:
                    k = len(combination)
                    r = calculate_redundancy_bits(k)
                    n = k + r

                    gx, n = select_generator_polynomial_for_file(k, r, n)
                    encoded = encode_for_file(combination, gx, n - k)
                    file.write(f"{combination} {encoded}\n")

        print("✓ Файл b.txt успешно создан!")
    except Exception as e:
        print(f"✗ Ошибка при создании файла b.txt: {e}")


def show_generator_steps(k, r, n):
    """Показать шаги выбора образующего многочлена"""
    _, _, steps = select_generator_polynomial(k, r, n, verbose=True)
    print("\n" + "=" * 60)
    print("ШАГИ ВЫБОРА ОБРАЗУЮЩЕГО МНОГОЧЛЕНА")
    print("=" * 60)
    print(steps)


def main():
    """Главная функция программы"""
    if len(sys.argv) > 1:
        # Режим генерации файлов
        arg = sys.argv[1].lower()
        if arg == "gx":
            generate_gx_file()
        elif arg == "b":
            generate_b_file()
        else:
            print("Неизвестный аргумент. Используйте:")
            print("  python main.py gx  - для генерации gx.txt")
            print("  python main.py b   - для генерации b.txt")
        return

    # Ввод последовательности
    original = input("Введите двоичную комбинацию для кодирования: ").strip()

    # Проверка ввода
    if not original or not all(c in "01" for c in original):
        print("Ошибка: введите корректную двоичную комбинацию (только 0 и 1)")
        return

    # Вывод начальной информации
    show_initial_info(original)

    # Кодирование
    encoded_combination, selected_polynomial, n = encode_combination(original)

    k = len(original)
    r_actual = n - k

    # Основной цикл выбора действий
    while True:
        print("\n" + "-" * 60)
        print("ВЫБЕРИТЕ ДЕЙСТВИЕ:")
        print(
            f"1 - Вывести шаги нахождения образующего многочлена (k={k}, r={r_actual}, n={n})"
        )
        print("2 - Ввести позицию ошибки для декодирования")
        print("0 - Выход")
        print("-" * 60)

        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            r_initial = calculate_redundancy_bits(k)
            show_generator_steps(k, r_initial, n)

        elif choice == "2":
            try:
                error_pos = int(
                    input(
                        f"Введите позицию для ошибки (1-{len(encoded_combination)}): "
                    ).strip()
                )

                if error_pos < 1 or error_pos > len(encoded_combination):
                    print(
                        f"Ошибка: позиция должна быть от 1 до {len(encoded_combination)}"
                    )
                    continue

                erroneous = introduce_error(encoded_combination, error_pos)
                corrected = decode_and_correct(
                    erroneous, selected_polynomial, encoded_combination
                )

                # Извлекаем информационные биты
                info_bits = corrected[: len(encoded_combination) - r_actual]
                print(f"\n" + "=" * 60)
                print("ИТОГОВЫЙ РЕЗУЛЬТАТ")
                print("=" * 60)
                print(f"Исправленная комбинация: {corrected}")
                print(f"Информационные биты: {info_bits}")

                # После исправления ошибки завершаем работу
                break

            except ValueError:
                print("Ошибка: введите число")

        elif choice == "0":
            print("Выход из программы...")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
