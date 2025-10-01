import math
import matplotlib.pyplot as plt

def calculate_entropy(probabilities):
    """
    Вычисление энтропии по формуле Шеннона.
    Формула: H(X) = -∑ p_i * log2(p_i)
    """
    entropy = 0.0
    for prob in probabilities:
        if prob > 0:
            entropy -= prob * math.log2(prob)
    return entropy

def task1():
    """
    Биномиальное распределение.
    Формула: P(k) = C(n,k) * p^k * (1-p)^(n-k)
    """
    n = int(input("Введите количество испытаний n: "))
    p_specific = float(input("Введите вероятность p: "))
    
    # Построение вероятностной схемы для конкретного p
    print("\nВероятностная схема:")
    print("k\tP(k)")
    probs_specific = []
    sum_prob = 0.0
    
    for k in range(0, n + 1):
        comb = math.comb(n, k)
        prob = comb * (p_specific ** k) * ((1 - p_specific) ** (n - k))
        probs_specific.append(prob)
        sum_prob += prob
        print(f"{k}\t{prob:.6f}")
    
    print(f"Сумма вероятностей: {sum_prob:.6f}")
    
    # Расчет энтропии для конкретного p
    H_specific = calculate_entropy(probs_specific)
    print(f"Энтропия H(p) для n={n}, p={p_specific}: {H_specific:.6f} бит")
    
    # Построение графика
    p_values = []
    H_values = []
    
    for i in range(1000):
        p = i / 1000.0
        p_values.append(p)
        
        # Формирование вероятностей для каждого k
        probs = []
        for k in range(0, n + 1):
            comb = math.comb(n, k)
            prob = comb * (p ** k) * ((1 - p) ** (n - k))
            probs.append(prob)
        
        H = calculate_entropy(probs)
        H_values.append(H)
    
    # Анализ экстремумов
    max_H = max(H_values)
    max_index = H_values.index(max_H)
    
    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(p_values, H_values, label='H(p)')
    plt.scatter(p_values[max_index], H_values[max_index], color='red', label='Максимум')
    plt.scatter(0, 0, color='green', label='Минимум')
    plt.scatter(1, 0, color='green')
    plt.xlabel('Вероятность p')
    plt.ylabel('Энтропия H(p)')
    plt.title('Энтропия биномиального распределения')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    print(f"Максимальное значение энтропии: H({p_values[max_index]:.3f}) = {H_values[max_index]:.3f}")
    print("Минимальные значения энтропии: H(0) = 0, H(1) = 0")

def task2():
    """
    Геометрическое распределение.
    Формула: P(k) = (1-p)^(k-1) * p
    """
    # Запрос вероятности p у пользователя
    p_specific = float(input("Введите вероятность p: "))
    
    # Вывод вероятностной схемы для конкретного p
    print("\nВероятностная схема (геометрическое распределение):")
    print("k\tP(k)")
    probs_specific = []
    k = 1
    sum_prob = 0.0
    epsilon = 1e-9
    
    while True:
        prob = (1 - p_specific) ** (k - 1) * p_specific
        if prob < epsilon:
            break
        probs_specific.append(prob)
        sum_prob += prob
        print(f"{k}\t{prob:.6f}")
        k += 1
    
    print(f"Сумма вероятностей: {sum_prob:.6f}")
    
    # Расчет энтропии для конкретного p
    H_specific = calculate_entropy(probs_specific)
    print(f"Энтропия H(p) для p={p_specific}: {H_specific:.6f} бит")
    
    # Построение графика энтропии в зависимости от p
    H_values = []
    p_values = []
    
    for i in range(1, 1000):
        p = i / 1000.0
        p_values.append(p)
        
        # Формирование распределения до достижения малой вероятности
        probs = []
        k = 1
        while True:
            prob = (1 - p) ** (k - 1) * p
            if prob < epsilon:
                break
            probs.append(prob)
            k += 1
        
        # Нормализация вероятностей
        sum_probs = sum(probs)
        normalized_probs = [prob / sum_probs for prob in probs]
        
        H = calculate_entropy(normalized_probs)
        H_values.append(H)
    
    # Анализ экстремумов
    max_H = max(H_values)
    max_index = H_values.index(max_H)
    
    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(p_values, H_values, label='H(p)')
    plt.scatter(p_values[max_index], H_values[max_index], color='red', label='Максимум')
    plt.xlabel('Вероятность p')
    plt.ylabel('Энтропия H(p)')
    plt.title('Энтропия геометрического распределения')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    print(f"Максимальное значение энтропии: H({p_values[max_index]:.3f}) = {H_values[max_index]:.3f}")
    print("Энтропия стремится к 0 при p -> 0+ и p -> 1-")

def task3():
    """
    Гипергеометрическое распределение.
    Формула: P(i) = [C(k,i) * C(n-k, m-i)] / C(n, m)
    """
    n = int(input("Введите размер партии n: "))
    m = int(input("Введите размер выборки m: "))
    k_specific = int(input("Введите количество стандартных изделий k: "))
    
    # Вывод вероятностной схемы для конкретного k
    print(f"\nВероятностная схема (гипергеометрическое распределение) для n={n}, m={m}, k={k_specific}:")
    print("i\tP(i)")
    
    # Определение допустимых значений i
    low = max(0, m - (n - k_specific))
    high = min(k_specific, m)
    
    # Вычисление вероятностей для каждого i
    probs_specific = []
    sum_prob = 0.0
    
    for i in range(low, high + 1):
        numerator = math.comb(k_specific, i) * math.comb(n - k_specific, m - i)
        denominator = math.comb(n, m)
        prob = numerator / denominator
        probs_specific.append(prob)
        sum_prob += prob
        print(f"{i}\t{prob:.6f}")
    
    print(f"Сумма вероятностей: {sum_prob:.6f}")
    
    # Расчет энтропии для конкретного k
    H_specific = calculate_entropy(probs_specific)
    print(f"Энтропия H(k) для k={k_specific}: {H_specific:.6f} бит")
    
    # Построение графика энтропии в зависимости от k
    H_values = []
    k_values = list(range(0, n + 1))
    
    for k in k_values:
        # Определение допустимых значений i
        low = max(0, m - (n - k))
        high = min(k, m)
        
        # Вычисление вероятностей для каждого i
        probs = []
        for i in range(low, high + 1):
            numerator = math.comb(k, i) * math.comb(n - k, m - i)
            denominator = math.comb(n, m)
            prob = numerator / denominator
            probs.append(prob)
        
        H = calculate_entropy(probs)
        H_values.append(H)
    
    # Анализ экстремумов
    max_H = max(H_values)
    max_index = H_values.index(max_H)
    
    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(k_values, H_values, label='H(k)')
    plt.scatter(k_values[max_index], H_values[max_index], color='red', label='Максимум')
    
    # Добавляем точки минимума
    if H_values[0] == 0:
        plt.scatter(k_values[0], H_values[0], color='green', label='Минимум')
    if H_values[-1] == 0:
        plt.scatter(k_values[-1], H_values[-1], color='green')
    
    plt.xlabel('Количество стандартных изделий k')
    plt.ylabel('Энтропия H(k)')
    plt.title('Энтропия гипергеометрического распределения')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    print(f"Максимальное значение энтропии: H({k_values[max_index]}) = {H_values[max_index]:.3f}")
    print("Минимальные значения энтропии достигаются на краях интервала")

def main():
    """
    Основное меню для выбора задачи
    """
    while True:
        print("\nВыберите задачу:")
        print("1. Биномиальное распределение")
        print("2. Геометрическое распределение")
        print("3. Гипергеометрическое распределение")
        print("4. Выход")
        choice = input("Ваш выбор (1-4): ")

        if choice == '1':
            task1()
        elif choice == '2':
            task2()
        elif choice == '3':
            task3()
        elif choice == '4':
            break
        else:
            print("Неверный ввод. Пожалуйста, выберите 1-4.")

if __name__ == "__main__":
    main()