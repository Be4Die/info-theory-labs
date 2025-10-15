import math

def calculate_entropy(probabilities):
    """Вычисление энтропии H(X) = -Σ p(x)·log₂ p(x)"""
    entropy = 0
    for i in range(len(probabilities)):
        p = probabilities[i]
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy

def main():
    print("1 - Ввод с клавиатуры")
    print("2 - Загрузка из файла")
    choice = input("Выбор: ")
    
    message = ""
    
    if choice == "1":
        message = input("Введите сообщение: ")
    elif choice == "2":
        filename = input("Введите имя файла: ")
        try:
            file = open(filename, 'r', encoding='utf-8')
            message = file.read().strip()
            file.close()
        except FileNotFoundError:
            print("Файл не найден!")
            return
    else:
        print("Неверный выбор!")
        return
    
    if len(message) == 0:
        print("Сообщение пустое!")
        return
    
    # Обработка одиночных символов
    single_chars = list(message)
    total_chars = len(single_chars)
    
    # Подсчет частот одиночных символов
    single_counter = {}
    for i in range(total_chars):
        char = single_chars[i]
        if char in single_counter:
            single_counter[char] += 1
        else:
            single_counter[char] = 1
    
    # Вероятности одиночных символов
    single_probs = {}
    single_prob_list = []
    chars = list(single_counter.keys())
    for i in range(len(chars)):
        char = chars[i]
        prob = single_counter[char] / total_chars
        single_probs[char] = prob
        single_prob_list.append(prob)
    
    # Обработка пар символов
    pairs = []
    for i in range(len(message) - 1):
        pair = message[i:i+2]
        pairs.append(pair)
    
    total_pairs = len(pairs)
    
    # Подсчет частот пар символов
    pair_counter = {}
    for i in range(total_pairs):
        pair = pairs[i]
        if pair in pair_counter:
            pair_counter[pair] += 1
        else:
            pair_counter[pair] = 1
    
    # Вероятности пар символов
    pair_probs = {}
    pair_prob_list = []
    pair_keys = list(pair_counter.keys())
    for i in range(len(pair_keys)):
        pair = pair_keys[i]
        prob = pair_counter[pair] / total_pairs
        pair_probs[pair] = prob
        pair_prob_list.append(prob)
    
    # Сортировка одиночных символов по частоте (убывание)
    sorted_singles = []
    for char, count in single_counter.items():
        sorted_singles.append((char, count))
    
    # Сортировка по убыванию частоты
    sorted_singles.sort(key=lambda x: x[1], reverse=True)
    
    # Сортировка пар символов по частоте (убывание)
    sorted_pairs = []
    for pair, count in pair_counter.items():
        sorted_pairs.append((pair, count))
    
    # Сортировка по убыванию частоты
    sorted_pairs.sort(key=lambda x: x[1], reverse=True)
    
    # Вычисление энтропий
    H_X = calculate_entropy(single_prob_list)  # H(X) = -Σ p(x)·log₂ p(x)
    H_XY = calculate_entropy(pair_prob_list)   # H(XY) = -Σ p(x,y)·log₂ p(x,y)
    H_Y_X = H_XY - H_X  # H(Y|X) = H(XY) - H(X)
    I_Y_X = H_X - H_Y_X  # I(Y,X) = H(X) - H(Y|X)
    
    # Вычисление избыточностей
    m = len(single_probs)  # количество различных символов
    
    # Длина кода при равномерном кодировании через логарифм по основанию 2
    if m > 0:
        l = math.ceil(math.log2(m))
    else:
        l = 0
    
    # D₀ = 1 - (log₂ m / l) - избыточность округления
    if m > 0:
        D0 = 1 - (math.log2(m) / l)
    else:
        D0 = 0
    
    # Dₚ = 1 - H(X) / log₂ m - избыточность неравномерности
    if m > 1:
        Dp = 1 - (H_X / math.log2(m))
    else:
        Dp = 0
    
    # Dₛ = 1 - H(Y|X) / H(X) - избыточность статистической связи
    if H_X > 0:
        Ds = 1 - (H_Y_X / H_X)
    else:
        Ds = 0
    
    # D = Dₚ + Dₛ - Dₚ·Dₛ - полная избыточность
    D = Dp + Ds - Dp * Ds
    
    # Вывод результатов
    print("\n" + "=" * 40)
    print("РЕЗУЛЬТАТЫ ОБРАБОТКИ")
    print("=" * 40)
    
    # Одиночные символы
    print("\nОДИНОЧНЫЕ СИМВОЛЫ")
    print("-" * 50)
    print("№   Символ   Частота  Вероятность")
    print("-" * 50)
    
    for i in range(len(sorted_singles)):
        char = sorted_singles[i][0]
        count = sorted_singles[i][1]
        prob = single_probs[char]
        print(f"{i+1:<3} {char:<8} {count:<8} {prob:<12.6f}")
    
    # Пары символов
    print("\nПАРЫ СИМВОЛОВ")
    print("-" * 50)
    print("№   Символ   Частота  Вероятность")
    print("-" * 50)
    
    for i in range(len(sorted_pairs)):
        pair = sorted_pairs[i][0]
        count = sorted_pairs[i][1]
        prob = pair_probs[pair]
        print(f"{i+1:<3} {pair:<8} {count:<8} {prob:<12.6f}")
    
    # Статистические характеристики
    print("\nСТАТИСТИЧЕСКИЕ ХАРАКТЕРИСТИКИ")
    print("-" * 40)
    print(f"Энтропия H(X): {H_X:.6f} бит")
    print("  H(X) = -Σ p(x)·log₂ p(x)")
    print(f"Энтропия H(XY): {H_XY:.6f} бит")
    print("  H(XY) = -Σ p(x,y)·log₂ p(x,y)")
    print(f"Условная энтропия H(Y|X): {H_Y_X:.6f} бит")
    print("  H(Y|X) = H(XY) - H(X)")
    print(f"Количество информации I(Y,X): {I_Y_X:.6f} бит")
    print("  I(Y,X) = H(X) - H(Y|X)")
    
    # Избыточности
    print("\nИЗБЫТОЧНОСТИ")
    print("-" * 40)
    print(f"Избыточность округления D0: {D0:.6f}")
    print("  D₀ = 1 - (log₂ m / l)")
    print(f"Избыточность неравномерности Dp: {Dp:.6f}")
    print("  Dₚ = 1 - H(X) / log₂ m")
    print(f"Избыточность статистической связи Ds: {Ds:.6f}")
    print("  Dₛ = 1 - H(Y|X) / H(X)")
    print(f"Полная избыточность D: {D:.6f}")
    print("  D = Dₚ + Dₛ - Dₚ·Dₛ")
    
    print(f"\nДлина сообщения: {total_chars} символов")
    print(f"Количество различных символов: {m}")
    print(f"Длина равномерного кода: {l}")

if __name__ == "__main__":
    main()