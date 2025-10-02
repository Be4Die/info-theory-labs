import math
import os

def read_message():
    print("Выберите способ ввода:")
    print("1 - Ввод с клавиатуры")
    print("2 - Чтение из файла")
    
    choice = input("Ваш выбор (1/2): ")
    choice = choice.strip()
    
    if choice == '1':
        message = input("Введите сообщение: ")
        return message.strip()
    elif choice == '2':
        filename = input("Введите имя файла: ")
        filename = filename.strip()
        try:
            file = open(filename, 'r', encoding='utf-8')
            content = file.read()
            file.close()
            return content.strip()
        except:
            print("Ошибка при чтении файла!")
            return read_message()
    else:
        print("Неверный выбор!")
        return read_message()

def calculate_entropy(prob_dict):
    entropy = 0.0
    keys = list(prob_dict.keys())
    for i in range(len(keys)):
        key = keys[i]
        prob = prob_dict[key]
        if prob > 0:
            entropy = entropy - prob * math.log2(prob)
    return entropy

def count_chars(message):
    char_count = {}
    for i in range(len(message)):
        char = message[i]
        if char in char_count:
            char_count[char] = char_count[char] + 1
        else:
            char_count[char] = 1
    return char_count

def count_bigrams(message):
    bigram_count = {}
    for i in range(len(message) - 1):
        bigram = message[i:i+2]
        if bigram in bigram_count:
            bigram_count[bigram] = bigram_count[bigram] + 1
        else:
            bigram_count[bigram] = 1
    return bigram_count

def calculate_probabilities(count_dict, total):
    prob_dict = {}
    keys = list(count_dict.keys())
    for i in range(len(keys)):
        key = keys[i]
        prob_dict[key] = count_dict[key] / total
    return prob_dict

def sort_by_probability(prob_dict):
    items = []
    keys = list(prob_dict.keys())
    for i in range(len(keys)):
        key = keys[i]
        items.append((key, prob_dict[key]))
    
    # Сортировка по убыванию вероятности
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i][1] < items[j][1]:
                temp = items[i]
                items[i] = items[j]
                items[j] = temp
            elif items[i][1] == items[j][1] and items[i][0] > items[j][0]:
                temp = items[i]
                items[i] = items[j]
                items[j] = temp
    return items

def print_table(items, title, is_bigram=False):
    print("\n" + title)
    print("----------------------------------------")
    if is_bigram:
        print("№   Сочетание   Частота   Вероятность")
        for i in range(len(items)):
            item = items[i]
            print("%-3d %-10s %-9d %-12.6f" % (i + 1, item[0], item[1], item[2]))
    else:
        print("№   Символ   Частота   Вероятность")
        for i in range(len(items)):
            item = items[i]
            char_display = item[0]
            if char_display == ' ':
                char_display = '[space]'
            elif char_display == '\n':
                char_display = '[newline]'
            elif char_display == '\t':
                char_display = '[tab]'
            print("%-3d %-8s %-9d %-12.6f" % (i + 1, char_display, item[1], item[2]))

def analyze_message(message):
    # Анализ одиночных символов
    char_count = count_chars(message)
    total_chars = len(message)
    char_probs = calculate_probabilities(char_count, total_chars)
    
    # Анализ биграмм
    bigram_count = count_bigrams(message)
    total_bigrams = len(message) - 1
    bigram_probs = calculate_probabilities(bigram_count, total_bigrams)
    
    # Расчет энтропий
    H_X = calculate_entropy(char_probs)
    H_XY = calculate_entropy(bigram_probs)
    
    # Условная энтропия и взаимная информация
    H_Y_given_X = H_XY - H_X
    I_Y_X = H_X - H_Y_given_X
    
    # Длина кода при равномерном кодировании
    m = len(char_count)
    if m > 0:
        l_uniform = math.ceil(math.log2(m))
    else:
        l_uniform = 0
    
    # Избыточности
    if m > 0:
        H_max = math.log2(m)
        D_p = 1 - H_X / H_max
    else:
        H_max = 0
        D_p = 0
    
    if H_X > 0:
        D_s = 1 - H_Y_given_X / H_X
    else:
        D_s = 0
    
    D_total = D_p + D_s - D_p * D_s
    
    # Подготовка данных для вывода
    char_items = []
    char_keys = list(char_count.keys())
    for i in range(len(char_keys)):
        key = char_keys[i]
        char_items.append((key, char_count[key], char_probs[key]))
    
    bigram_items = []
    bigram_keys = list(bigram_count.keys())
    for i in range(len(bigram_keys)):
        key = bigram_keys[i]
        bigram_items.append((key, bigram_count[key], bigram_probs[key]))
    
    # Сортировка
    sorted_chars = sort_by_probability(char_probs)
    sorted_bigrams = sort_by_probability(bigram_probs)
    
    # Преобразование обратно в формат для вывода
    sorted_char_items = []
    for i in range(len(sorted_chars)):
        char, prob = sorted_chars[i]
        sorted_char_items.append((char, char_count[char], prob))
    
    sorted_bigram_items = []
    for i in range(len(sorted_bigrams)):
        bigram, prob = sorted_bigrams[i]
        sorted_bigram_items.append((bigram, bigram_count[bigram], prob))
    
    return {
        'sorted_chars': sorted_char_items,
        'sorted_bigrams': sorted_bigram_items,
        'H_X': H_X,
        'H_XY': H_XY,
        'H_Y_given_X': H_Y_given_X,
        'I_Y_X': I_Y_X,
        'l_uniform': l_uniform,
        'D_p': D_p,
        'D_s': D_s,
        'D_total': D_total
    }

def main():
    print("Лабораторная работа №2: 'Обработка алфавита введенного сообщения'")
    print("==========================================================")
    
    message = read_message()
    
    if len(message) == 0:
        print("Сообщение пусто!")
        return
    
    print("\nАнализируемое сообщение: ", end="")
    if len(message) > 100:
        print(message[:100] + "...")
    else:
        print(message)
    print("Длина сообщения: %d символов" % len(message))
    
    results = analyze_message(message)
    
    # Вывод таблиц
    print_table(results['sorted_chars'], "СТАТИСТИКА СИМВОЛОВ (по убыванию вероятности)")
    print_table(results['sorted_bigrams'], "СТАТИСТИКА ДВУХСИМВОЛЬНЫХ СОЧЕТАНИЙ", True)
    
    # Вывод результатов расчетов
    print("\nРЕЗУЛЬТАТЫ РАСЧЕТОВ:")
    print("----------------------------------------")
    print("Энтропия на один символ (H(X)): %.4f бит" % results['H_X'])
    print("Энтропия на одно двухсимвольное сочетание (H(XY)): %.4f бит" % results['H_XY'])
    print("Условная энтропия (H(Y|X)): %.4f бит" % results['H_Y_given_X'])
    print("Взаимная информация (I(Y,X)): %.4f бит" % results['I_Y_X'])
    print("Длина кода при равномерном кодировании: %d бит" % results['l_uniform'])
    print("Избыточность из-за неравномерности (D_p): %.4f" % results['D_p'])
    print("Избыточность из-за статистической связи (D_s): %.4f" % results['D_s'])
    print("Полная информационная избыточность (D): %.4f" % results['D_total'])

if __name__ == "__main__":
    main()