import numpy as np
import matplotlib.pyplot as plt
import math

def calculate_entropy(probabilities):
    """
    Вычисление энтропии по формуле Шеннона.
    Формула: H(X) = -∑ p_i * log2(p_i) (Определение 1.3 из пособия)
    """
    prob_non_zero = probabilities[probabilities > 0]
    return -np.sum(prob_non_zero * np.log2(prob_non_zero))

def task_binomial():
    """
    Биномиальное распределение.
    Формула: P(k) = C(n,k) * p^k * (1-p)^(n-k)
    Энтропия вычисляется для каждого p на основе распределения
    """
    n = int(input("Введите количество испытаний n: "))
    
    # Запрос конкретного значения p у пользователя
    while True:
        p_specific = float(input("Введите конкретное значение p (0 ≤ p ≤ 1): "))
        if 0 <= p_specific <= 1:
            break
        print("Ошибка: p должно быть между 0 и 1.")
    
    # Вычисление вероятностей для конкретного p
    k_values = np.arange(0, n+1)
    probs_specific = np.array([math.comb(n, k) * (p_specific ** k) * ((1 - p_specific) ** (n - k)) for k in k_values])
    H_specific = calculate_entropy(probs_specific)
    
    # Вывод вероятностной схемы
    print("\nВероятностная схема для p = {:.3f}:".format(p_specific))
    print("k\tP(k)")
    for k, prob in zip(k_values, probs_specific):
        print("{}\t{:.5f}".format(k, prob))
    print("Энтропия H({:.3f}) = {:.3f}".format(p_specific, H_specific))
    
    # Построение графика для диапазона p
    p_values = np.linspace(0, 1, 1000)
    H_values = []
    
    for p in p_values:
        probs = np.array([math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k)) for k in k_values])
        H = calculate_entropy(probs)
        H_values.append(H)
    
    # Анализ экстремумов (максимум и минимумы)
    H_values = np.array(H_values)
    max_index = np.argmax(H_values)
    min_indices = np.where(H_values == 0)[0]
    
    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(p_values, H_values, label='H(p)')
    plt.scatter(p_values[max_index], H_values[max_index], color='red', label='Максимум')
    if len(min_indices) > 0:
        for idx in min_indices:
            plt.scatter(p_values[idx], H_values[idx], color='green', label='Минимум')
    plt.xlabel('Вероятность p')
    plt.ylabel('Энтропия H(p)')
    plt.title('Энтропия биномиального распределения')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    print(f"Максимальное значение энтропии: H({p_values[max_index]:.3f}) = {H_values[max_index]:.3f}")
    print("Минимальные значения энтропии: H(0) = 0, H(1) = 0")

def task_geometric():
    """
    Геометрическое распределение.
    Формула: P(k) = (1-p)^(k-1) * p
    Энтропия вычисляется для усеченного распределения (до вероятности < epsilon)
    """
    # Запрос конкретного значения p у пользователя
    while True:
        p_specific = float(input("Введите конкретное значение p (0 < p ≤ 1): "))
        if 0 < p_specific <= 1:
            break
        print("Ошибка: p должно быть между 0 и 1 (исключая 0).")
    
    # Вычисление вероятностей для конкретного p
    k = 1
    probs_specific = []
    epsilon = 1e-9
    
    # Формирование распределения до достижения малой вероятности
    while True:
        prob = (1 - p_specific) ** (k - 1) * p_specific
        if prob < epsilon:
            break
        probs_specific.append(prob)
        k += 1
        if k > 10000:  # Защита от бесконечного цикла
            break
    
    # Нормализация вероятностей (сумма должна быть равна 1)
    probs_specific = np.array(probs_specific)
    probs_specific = probs_specific / np.sum(probs_specific)
    H_specific = calculate_entropy(probs_specific)
    
    # Вывод вероятностной схемы
    print("\nВероятностная схема для p = {:.3f}:".format(p_specific))
    print("k\tP(k)")
    for i, prob in enumerate(probs_specific, 1):
        print("{}\t{:.5f}".format(i, prob))
    print("Энтропия H({:.3f}) = {:.3f}".format(p_specific, H_specific))
    
    # Построение графика для диапазона p
    p_values = np.linspace(0.001, 1, 1000)
    H_values = []
    
    for p in p_values:
        k = 1
        probs = []
        # Формирование распределения до достижения малой вероятности
        while True:
            prob = (1 - p) ** (k - 1) * p
            if prob < epsilon:
                break
            probs.append(prob)
            k += 1
            if k > 1000:  # Защита от бесконечного цикла
                break
        probs = np.array(probs)
        probs = probs / np.sum(probs)  # Нормализация
        H = calculate_entropy(probs)
        H_values.append(H)
    
    # Анализ экстремумов
    H_values = np.array(H_values)
    max_index = np.argmax(H_values)
    
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

def task_hypergeometric():
    """
    Гипергеометрическое распределение.
    Формула: P(i) = [C(k,i) * C(n-k, m-i)] / C(n, m)
    Энтропия вычисляется для каждого k
    """
    n = int(input("Введите размер партии n: "))
    m = int(input("Введите размер выборки m: "))
    k_values = np.arange(0, n+1)
    H_values = []
    
    for k in k_values:
        # Определение допустимых значений i
        low = max(0, m - (n - k))
        high = min(k, m)
        i_values = np.arange(low, high+1)
        # Вычисление вероятностей для каждого i
        probs = np.array([math.comb(k, i) * math.comb(n - k, m - i) / math.comb(n, m) for i in i_values])
        H = calculate_entropy(probs)
        H_values.append(H)
    
    # Анализ экстремумов
    H_values = np.array(H_values)
    max_index = np.argmax(H_values)
    min_indices = np.where(H_values == 0)[0]
    
    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(k_values, H_values, label='H(k)')
    plt.scatter(k_values[max_index], H_values[max_index], color='red', label='Максимум')
    if len(min_indices) > 0:
        for idx in min_indices:
            plt.scatter(k_values[idx], H_values[idx], color='green', label='Минимум')
    plt.xlabel('Количество стандартных изделий k')
    plt.ylabel('Энтропия H(k)')
    plt.title('Энтропия гипергеометрического распределения')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    print(f"Максимальное значение энтропии: H({k_values[max_index]}) = {H_values[max_index]:.3f}")
    print("Минимальные значения энтропии достигаются на краях интервала")

def entropy_poisson(a):
    """
    Вычисление энтропии распределения Пуассона.
    Формула: P(k) = (a^k * e^{-a}) / k!
    Вычисляется до достижения малой вероятности
    """
    if a == 0:
        return 0.0
    probs = []
    p = math.exp(-a)
    probs.append(p)
    k = 1
    # Формирование распределения Пуассона
    while True:
        p = p * a / k
        if p < 1e-9 and k > a:
            break
        probs.append(p)
        k += 1
        if k > 1000:  # Защита от бесконечного цикла
            break
    probs = np.array(probs)
    return calculate_entropy(probs)

def task_poisson_time():
    """
    Зависимость энтропии Пуассона от времени.
    Параметр: λt (лямбда * время)
    """
    lambda_val = float(input("Введите интенсивность потока λ: "))
    t_values = np.linspace(0.001, 5 * lambda_val, 1000)
    H_values = [entropy_poisson(lambda_val * t) for t in t_values]
    
    # Анализ экстремумов
    H_values = np.array(H_values)
    max_index = np.argmax(H_values)
    
    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(t_values, H_values, label='H(t)')
    plt.scatter(t_values[max_index], H_values[max_index], color='red', label='Максимум')
    plt.xlabel('Время t')
    plt.ylabel('Энтропия H(t)')
    plt.title('Энтропия пуассоновского распределения (зависимость от t)')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    print(f"Максимальное значение энтропии: H({t_values[max_index]:.3f}) = {H_values[max_index]:.3f}")

def task_poisson_lambda():
    """
    Зависимость энтропии Пуассона от интенсивности.
    Параметр: λt (лямбда * время)
    """
    t_val = float(input("Введите время t: "))
    lambda_values = np.linspace(0.001, 3 * t_val, 1000)
    H_values = [entropy_poisson(l * t_val) for l in lambda_values]
    
    # Анализ экстремумов
    H_values = np.array(H_values)
    max_index = np.argmax(H_values)
    
    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(lambda_values, H_values, label='H(λ)')
    plt.scatter(lambda_values[max_index], H_values[max_index], color='red', label='Максимум')
    plt.xlabel('Интенсивность λ')
    plt.ylabel('Энтропия H(λ)')
    plt.title('Энтропия пуассоновского распределения (зависимость от λ)')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    print(f"Максимальное значение энтропии: H({lambda_values[max_index]:.3f}) = {H_values[max_index]:.3f}")

def main():
    """
    Основное меню для выбора задачи
    Соответствует практической части Лабораторной работы №1
    """
    while True:
        print("\nВыберите задачу:")
        print("1. Биномиальное распределение")
        print("2. Геометрическое распределение")
        print("3. Гипергеометрическое распределение")
        print("4. Пуассоновское распределение (зависимость от времени)")
        print("5. Пуассоновское распределение (зависимость от интенсивности)")
        print("6. Выход")
        choice = input("Ваш выбор (1-6): ")

        if choice == '1':
            task_binomial()  # Задача 1 из практической части
        elif choice == '2':
            task_geometric()  # Задача 2 из практической части
        elif choice == '3':
            task_hypergeometric()  # Задача 3 из практической части
        elif choice == '4':
            task_poisson_time()  # Задача 4 из практической части
        elif choice == '5':
            task_poisson_lambda()  # Задача 5 из практической части
        elif choice == '6':
            break
        else:
            print("Неверный ввод. Пожалуйста, выберите 1-6.")

if __name__ == "__main__":
    main()