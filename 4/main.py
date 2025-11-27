import math

def input_binary_sequence(prompt):
    while True:
        s = input(prompt)
        if all(c in '01' for c in s):
            return [int(bit) for bit in s]
        print("Ошибка: введите последовательность из 0 и 1")

def print_matrix(matrix, title=None, decimal_header=False):
    if title:
        print(title)
    if decimal_header and matrix:
        header = [str(i+1) for i in range(len(matrix[0]))]
        print("    " + " ".join(f"{h:>3}" for h in header))
    for i, row in enumerate(matrix):
        if decimal_header:
            print(f"{i+1:2}| " + " ".join(f"{val:>3}" for val in row))
        else:
            print("   " + " ".join(f"{val:>3}" for val in row))

def identity_matrix(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def transpose_matrix(matrix):
    if not matrix:
        return []
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

def vector_multiply_matrix_gf2(vector, matrix):
    # Умножение вектора-строки на матрицу
    result = [0] * len(matrix[0])
    for j in range(len(matrix[0])):
        for i in range(len(vector)):
            result[j] ^= (vector[i] & matrix[i][j])
    return result

def matrix_multiply_vector_gf2(matrix, vector):
    # Умножение матрицы на вектор-столбец
    result = [0] * len(matrix)
    for i in range(len(matrix)):
        for j in range(len(vector)):
            result[i] ^= (matrix[i][j] & vector[j])
    return result

def main():
    # 1. Ввод исходной последовательности
    alpha = input_binary_sequence("Введите исходную последовательность (0 и 1): ")
    k = len(alpha)
    print(f"2. Число информационных разрядов k = {k}")
    
    # 3. Вычисление числа корректирующих разрядов
    r = math.ceil(math.log2(k + 1 + math.ceil(math.log2(k + 1))))
    print(f"3. Формула для r: ⌈log₂(k+1+⌈log₂(k+1)⌉)⌉ = ⌈log₂({k}+1+⌈log₂({k}+1)⌉)⌉ = {r}")
    
    # 4. Вычисление общей длины
    n = k + r
    print(f"4. n = k + r = {k} + {r} = {n}")
    
    # 5. Построение проверочной матрицы H
    print("\n5. Построение проверочной матрицы H:")
    
    # Генерация матрицы A
    A_columns = []
    column_numbers = []
    
    # Создаем столбцы для чисел от 1 до n, пропуская степени двойки
    for num in range(1, n + 1):
        # Пропускаем степени двойки (1, 2, 4, 8, ...)
        if (num & (num - 1)) == 0:  # Если степень двойки
            continue
        
        # Преобразуем число в двоичный формат с r битами
        binary = [int(b) for b in format(num, f'0{r}b')]
        A_columns.append(binary)
        column_numbers.append(num)
    
    # Транспонируем матрицу столбцов
    A = []
    if A_columns:
        for i in range(r):
            row = []
            for col in A_columns:
                row.append(col[i])
            A.append(row)
    
    print("Матрица A (с десятичными номерами столбцов):")
    if A and column_numbers:
        header = [str(num) for num in column_numbers]
        print("    " + " ".join(f"{h:>3}" for h in header))
        for i, row in enumerate(A):
            print(f"{i+1:2}| " + " ".join(f"{val:>3}" for val in row))
    
    # Единичная матрица E
    E = identity_matrix(r)
    print_matrix(E, "\nЕдиничная матрица E:")
    
    # Формирование H
    H = []
    for i in range(r):
        H.append(A[i] + E[i])
    print_matrix(H, "\nПроверочная матрица H = [A|E]:")
    
    # 6. Построение порождающей матрицы G
    print("\n6. Построение порождающей матрицы G:")
    E_k = identity_matrix(k)
    
    # Транспонируем матрицу A для получения Aᵀ
    A_transposed = []
    if A:
        for j in range(len(A[0])):
            row = []
            for i in range(len(A)):
                row.append(A[i][j])
            A_transposed.append(row)
    
    G = []
    for i in range(k):
        G.append(E_k[i] + A_transposed[i])
    print_matrix(G, "Порождающая матрица G = [E|Aᵀ]:")
    
    # 7. Кодирование последовательности
    beta = vector_multiply_matrix_gf2(alpha, G)
    print(f"\n7. Закодированная последовательность β = α * G:")
    print("   " + " ".join(f"{b:>3}" for b in beta))
    
    # 8. Проверка синдрома
    H_transposed = transpose_matrix(H)
    syndrome = vector_multiply_matrix_gf2(beta, H_transposed)
    print(f"\n8. Синдром S = β * Hᵀ:")
    print("   " + " ".join(f"{s:>3}" for s in syndrome))
    if all(s == 0 for s in syndrome):
        print("   Синдром нулевой - матрицы построены верно!")
    
    # 9. Ввод последовательности с ошибкой
    print("\n9. Формирование β' (с ошибкой):")
    print("0 - Ввести позицию ошибки")
    print("1 - Ввести полную последовательность")
    choice = input("Выбор: ")
    
    beta_prime = []
    manual_input = False
    if choice == '0':
        while True:
            try:
                pos = int(input(f"Введите позицию ошибки (1-{n}): "))
                if 1 <= pos <= n:
                    beta_prime = beta.copy()
                    beta_prime[pos-1] ^= 1  # Инвертируем бит
                    break
                else:
                    print("Неверная позиция")
            except ValueError:
                print("Введите число")
    else:
        beta_prime = input_binary_sequence(f"Введите β' (длина {n}): ")
        if len(beta_prime) != n:
            print(f"Ошибка: длина должна быть {n}")
            return
        manual_input = True
    
    print(f"   β': " + " ".join(f"{b:>3}" for b in beta_prime))
    
    # 10. Вычисление синдрома для β'
    syndrome_prime = vector_multiply_matrix_gf2(beta_prime, H_transposed)
    print(f"\n10. Синдром S' = β' * Hᵀ:")
    print("    " + " ".join(f"{s:>3}" for s in syndrome_prime))
    
    # 11. Поиск ошибки
    error_pos = None
    for col_idx in range(len(H[0])):
        # Получаем столбец из матрицы H
        column = []
        for row_idx in range(len(H)):
            column.append(H[row_idx][col_idx])
        
        # Сравниваем с синдромом
        if column == syndrome_prime:
            error_pos = col_idx + 1
            break
    
    if error_pos:
        print(f"11. Ошибка в позиции: {error_pos}")
        # 12. Исправление ошибки
        beta_corrected = beta_prime.copy()
        beta_corrected[error_pos-1] ^= 1
        print(f"12. Исправленная β: " + " ".join(f"{b:>3}" for b in beta_corrected))
        
        # Проверка, что исправленная последовательность совпадает с исходной
        if beta_corrected == beta:
            print("   ✓ Исправленная последовательность совпадает с исходной β")
        elif manual_input:
            print("   ✗ Исправленная последовательность НЕ совпадает с исходной β")
            print("   В последовательности допущено более одной ошибки, алгоритм не применим!")
    else:
        if all(s == 0 for s in syndrome_prime):
            print("11. Ошибка не обнаружена (синдром нулевой)")
            if manual_input and beta_prime != beta:
                print("   ✗ Последовательность не совпадает с исходной β")
                print("   В последовательности допущено более одной ошибки, алгоритм не применим!")
        else:
            print("11. Обнаружена ошибка, но позиция не определена")
            if manual_input:
                print("   В последовательности допущено более одной ошибки, алгоритм не применим!")
        print(f"12. Исходная β: " + " ".join(f"{b:>3}" for b in beta_prime))

if __name__ == "__main__":
    main()