import math

class BCHCode:
    """Класс для работы с кодами БЧХ"""
    
    # Таблица 1: Соотношение разрядов (n, k, r, s)
    TABLE_1 = {
        4: (7, 3, 1),
        5: (15, 10, 3),
        7: (15, 8, 2),
        11: (15, 4, 1),
        6: (31, 25, 7),
        26: (31, 5, 1),
        21: (31, 10, 2),
        16: (31, 15, 3),
        11: (31, 20, 5),
        57: (63, 6, 1),
        51: (63, 13, 2),
        45: (63, 18, 3),
        39: (63, 24, 4),
        36: (63, 27, 5),
        30: (63, 33, 6),
        24: (63, 39, 7),
        18: (63, 35, 10),
        16: (63, 37, 11),
        10: (63, 53, 13),
        7: (63, 56, 15),
        120: (127, 7, 1),
        113: (127, 14, 2),
        106: (127, 21, 3),
        99: (127, 28, 4),
        92: (127, 35, 5),
        85: (127, 42, 6),
        78: (127, 49, 7),
        71: (127, 56, 9),
        64: (127, 63, 10),
        57: (127, 70, 11),
        50: (127, 77, 13),
        43: (127, 84, 14),
        36: (127, 91, 15),
        29: (127, 98, 21),
        22: (127, 105, 23),
        15: (127, 112, 27),
        8: (127, 119, 31)
    }
    
    # Таблица 2: Минимальные многочлены в поле Галуа
    TABLE_2 = {
        2: {1: '111'},
        3: {1: '1011', 3: '1101'},
        4: {1: '10011', 3: '11111', 5: '111', 7: '11001'},
        5: {1: '100101', 3: '111101', 5: '110111', 7: '101111', 9: '110111', 11: '111011'},
        6: {1: '1000011', 3: '1010111', 5: '1100111', 7: '1001001', 9: '1101', 11: '1101101'}
    }
    
    @staticmethod
    def polynomial_multiply(poly1, poly2):
        """Умножение двоичных полиномов"""
        bits1 = [int(bit) for bit in poly1]
        bits2 = [int(bit) for bit in poly2]
        result_len = len(bits1) + len(bits2) - 1
        result = [0] * result_len
        
        for i in range(len(bits1)):
            for j in range(len(bits2)):
                result[i + j] ^= bits1[i] & bits2[j]
        
        return ''.join(str(bit) for bit in result)
    
    @staticmethod
    def polynomial_mod(dividend, divisor):
        """Деление двоичных полиномов с возвратом остатка"""
        dividend = dividend.lstrip('0') or '0'
        divisor = divisor.lstrip('0') or '0'
        
        if dividend == '0' or len(dividend) < len(divisor):
            remainder_len = len(divisor) - 1
            return '0' * remainder_len
        
        dividend_list = list(dividend)
        divisor_len = len(divisor)
        
        for i in range(len(dividend) - divisor_len + 1):
            if dividend_list[i] == '1':
                for j in range(divisor_len):
                    dividend_list[i + j] = str(int(dividend_list[i + j]) ^ int(divisor[j]))
        
        remainder = ''.join(dividend_list)[-(divisor_len - 1):]
        return remainder.zfill(divisor_len - 1)
    
    @staticmethod
    def binary_xor(bin1, bin2):
        """XOR двух двоичных строк"""
        max_len = max(len(bin1), len(bin2))
        bin1 = bin1.zfill(max_len)
        bin2 = bin2.zfill(max_len)
        return ''.join(str(int(a) ^ int(b)) for a, b in zip(bin1, bin2))
    
    @staticmethod
    def hamming_weight(binary_str):
        """Вычисление веса Хэмминга"""
        return binary_str.count('1')
    
    @staticmethod
    def cyclic_shift_left(binary_str, positions=1):
        """Циклический сдвиг влево"""
        positions = positions % len(binary_str)
        return binary_str[positions:] + binary_str[:positions]
    
    @staticmethod
    def cyclic_shift_right(binary_str, positions=1):
        """Циклический сдвиг вправо"""
        positions = positions % len(binary_str)
        return binary_str[-positions:] + binary_str[:-positions]
    
    def __init__(self):
        self.k = 0
        self.n = 0
        self.r = 0
        self.s = 0
        self.h = 0
        self.i = 0
        self.generator_poly = ""
        self.encoded_message = ""
        
    def find_parameters(self, k):
        """Поиск параметров кода для заданного k"""
        if k not in self.TABLE_1:
            available_k = sorted(self.TABLE_1.keys())
            raise ValueError(f"Для k={k} нет данных в таблице. Доступные значения: {available_k}")
        
        self.k = k
        self.n, self.r, self.s = self.TABLE_1[k]
        self.h = int(math.log2(self.n + 1))
        self.i = 2 * self.s - 1
        
        print(f"\nНайдены параметры кода БЧХ:")
        print(f"  k = {self.k} (число информационных разрядов)")
        print(f"  n = {self.n} (длина кодового слова)")
        print(f"  r = {self.r} (число проверочных разрядов)")
        print(f"  s = {self.s} (максимальное число исправляемых ошибок)")
        print(f"  h = log₂({self.n}+1) = {self.h} (старшая степень минимального многочлена)")
        print(f"  i = 2s-1 = 2*{self.s}-1 = {self.i}")
        
        return self.n, self.r, self.s
    
    def find_generator_polynomial(self):
        """Построение порождающего многочлена"""
        if self.h not in self.TABLE_2:
            raise ValueError(f"Для h={self.h} нет данных в таблице минимальных многочленов")
        
        # Выбираем минимальные многочлены с нечетными индексами до i
        polynomials_to_multiply = []
        print(f"\nВыбор минимальных многочленов для h={self.h}, i={self.i}:")
        
        for idx in range(1, self.i + 1, 2):
            if idx in self.TABLE_2[self.h]:
                poly = self.TABLE_2[self.h][idx]
                polynomials_to_multiply.append((idx, poly))
                print(f"  P{idx}(x) = {poly}")
        
        if not polynomials_to_multiply:
            raise ValueError(f"Не найдены минимальные многочлены для h={self.h}, i={self.i}")
        
        # Формируем строку для вывода: P1(x), P3(x), ..., P{i}(x)
        poly_indices = [f"P{idx}(x)" for idx, _ in polynomials_to_multiply]
        poly_list_str = ", ".join(poly_indices)
        
        print(f"\nВычисление порождающего многочлена g(x) = НОК({poly_list_str}):")
        
        # Вычисляем порождающий многочлен как произведение
        first_idx, first_poly = polynomials_to_multiply[0]
        result = first_poly
        print(f"  Начальное значение: g(x) = {result} (P{first_idx}(x))")
        
        for idx, poly in polynomials_to_multiply[1:]:
            print(f"  Умножаем на P{idx}(x) = {poly}:")
            print(f"    {result} * {poly}", end=" = ")
            result = self.polynomial_multiply(result, poly)
            print(f"{result}")
        
        self.generator_poly = result
        print(f"\nПорождающий многочлен: g(x) = {self.generator_poly}")
        print(f"  Длина: {len(self.generator_poly)} бит")
        
        return self.generator_poly
    
    def encode_message(self, info_combination):
        """Кодирование информационной комбинации"""
        if len(info_combination) != self.k:
            raise ValueError(f"Длина информационной комбинации должна быть {self.k}, а получено {len(info_combination)}")
        
        print(f"\nКодирование информационной комбинации α = {info_combination}:")
        print(f"  1. Умножаем α(x) на x^{self.r}:")
        print(f"     α(x) = {info_combination}")
        print(f"     x^{self.r} = 1 с {self.r} нулями")
        
        # Умножаем на x^r
        multiplied = info_combination + '0' * self.r
        print(f"     α(x) * x^{self.r} = {info_combination} * {'0'*self.r} = {multiplied}")
        
        print(f"\n  2. Делим α(x)*x^{self.r} на порождающий многочлен g(x):")
        print(f"     Делимое: {multiplied}")
        print(f"     Делитель (g(x)): {self.generator_poly}")
        
        # Делим на порождающий многочлен
        remainder = self.polynomial_mod(multiplied, self.generator_poly)
        print(f"     Остаток от деления: {remainder}")
        
        print(f"\n  3. Формируем кодовое слово β(x) = α(x)*x^{self.r} + остаток:")
        print(f"     {multiplied}")
        print(f"  +  {remainder.zfill(len(multiplied))}")
        
        # Складываем (XOR) чтобы получить кодовое слово
        encoded = self.binary_xor(multiplied, remainder)
        self.encoded_message = encoded
        
        print(f"     Результат: {encoded}")
        print(f"\nКодовая комбинация: β = {encoded}")
        print(f"Длина кодового слова: {len(encoded)} бит")
        
        return encoded
    
    def introduce_errors(self, encoded_message, error_positions):
        """Внесение ошибок в кодовое слово"""
        if not error_positions:
            print("Ошибки не вносятся")
            return encoded_message
        
        encoded_list = list(encoded_message)
        
        print(f"\nВнесение {len(error_positions)} ошибок:")
        print(f"Исходная комбинация: {encoded_message}")
        
        for pos in sorted(error_positions):
            if pos < 0 or pos >= len(encoded_message):
                raise ValueError(f"Некорректная позиция ошибки: {pos}")
            
            # Инвертируем бит
            old_bit = encoded_list[pos]
            encoded_list[pos] = '1' if old_bit == '0' else '0'
            print(f"  Позиция {pos}: {old_bit} → {encoded_list[pos]}")
        
        corrupted = ''.join(encoded_list)
        print(f"Комбинация с ошибками: {corrupted}")
        
        return corrupted
    
    def decode_and_correct(self, corrupted_message):
        """Декодирование и исправление ошибок"""
        print(f"\nАЛГОРИТМ ИСПРАВЛЕНИЯ ОШИБОК:")
        print(f"=============================")
        print(f"Исходная комбинация с ошибками: {corrupted_message}")
        print(f"Порождающий многочлен g(x): {self.generator_poly}")
        print(f"Максимальное число исправляемых ошибок s = {self.s}")
        print(f"\n1. ВЫЧИСЛЕНИЕ СИНДРОМА:")
        
        current_message = corrupted_message
        shift_count = 0
        
        print(f"\n   Итерация {shift_count + 1} (без сдвига):")
        print(f"   ------------------------------------")
        print(f"   Принятая комбинация: {current_message}")
        
        while True:
            # Делим текущую комбинацию на порождающий многочлен
            remainder = self.polynomial_mod(current_message, self.generator_poly)
            weight = self.hamming_weight(remainder)
            
            print(f"   Делим на g(x) = {self.generator_poly}")
            print(f"   Получен остаток: {remainder}")
            print(f"   Вес остатка w = {weight}")
            
            # Проверяем вес остатка
            if weight <= self.s:
                print(f"\n   ✓ Найден образец ошибки с весом {weight} ≤ {self.s}!")
                print(f"\n2. ИСПРАВЛЕНИЕ ОШИБОК:")
                print(f"   -------------------")
                
                # Исправляем ошибку
                corrected = self.binary_xor(current_message, remainder)
                print(f"   Выполняем операцию XOR комбинации с остатком:")
                print(f"   {current_message}")
                print(f"   ⊕ {remainder.zfill(len(current_message))}")
                print(f"   = {corrected}")
                
                # Возвращаем циклический сдвиг
                if shift_count > 0:
                    print(f"\n3. ВОЗВРАТ ЦИКЛИЧЕСКОГО СДВИГА:")
                    print(f"   -----------------------------")
                    corrected = self.cyclic_shift_right(corrected, shift_count)
                    print(f"   Исправленная комбинация после возврата сдвига: {corrected}")
                
                # Проверка результата
                final_remainder = self.polynomial_mod(corrected, self.generator_poly)
                final_weight = self.hamming_weight(final_remainder)
                
                
                if final_weight == 0:
                    print(f"   ✓ Ошибки успешно исправлены!")
                else:
                    print(f"   ✗ Ошибки не полностью исправлены")
                
                return corrected
            
            # Если вес остатка больше s, продолжаем сдвигать
            if shift_count >= self.n - 1:
                print(f"\n✗ Не удалось исправить ошибки (превышено максимальное число сдвигов {self.n-1})!")
                print(f"  Это означает, что количество ошибок превышает корректирующую способность кода s={self.s}")
                return corrupted_message
            
            # Сдвигаем влево для следующей итерации
            shift_count += 1
            current_message = self.cyclic_shift_left(current_message)
            
            print(f"\n   Вес остатка {weight} > {self.s}, поэтому выполняем циклический сдвиг влево.")
            print(f"\n   Итерация {shift_count + 1} (сдвиг {shift_count}):")
            print(f"   ------------------------------------")
            print(f"   Комбинация после сдвига: {current_message}")


def main():
    """Основная функция приложения"""
    codec = BCHCode()
    
    print("=" * 60)
    print("КОДЫ БЧХ: КОДИРОВАНИЕ И ИСПРАВЛЕНИЕ ОШИБОК")
    print("=" * 60)
    
    while True:
        print("\n" + "=" * 60)
        print("МЕНЮ:")
        print("1. Закодировать информационную комбинацию")
        print("2. Выйти из приложения")
        print("=" * 60)
        
        choice = input("\nВыберите действие (1-2): ").strip()
        
        if choice == '1':
            try:
                # Ввод информационной комбинации
                info_combo = input("\nВведите информационную комбинацию (двоичная строка): ").strip()
                
                if not info_combo:
                    print("Ошибка: комбинация не может быть пустой")
                    continue
                    
                if not all(bit in '01' for bit in info_combo):
                    print("Ошибка: комбинация должна содержать только символы '0' и '1'")
                    continue
                
                k = len(info_combo)
                
                # Проверяем, есть ли параметры для такого k
                if k not in codec.TABLE_1:
                    available_k = sorted(codec.TABLE_1.keys())
                    print(f"\nОшибка: для k={k} нет данных в таблице")
                    print(f"Доступные значения k: {available_k}")
                    print("Пожалуйста, введите комбинацию другой длины")
                    continue
                
                print("\n" + "=" * 60)
                print("РАСЧЕТ ПАРАМЕТРОВ КОДА БЧХ")
                print("=" * 60)
                
                # Находим параметры кода
                n, r, s = codec.find_parameters(k)
                
                print("\n" + "=" * 60)
                print("ПОСТРОЕНИЕ ПОРОЖДАЮЩЕГО МНОГОЧЛЕНА")
                print("=" * 60)
                
                # Строим порождающий многочлен
                g = codec.find_generator_polynomial()
                
                print("\n" + "=" * 60)
                print("КОДИРОВАНИЕ СООБЩЕНИЯ")
                print("=" * 60)
                
                # Кодируем сообщение
                encoded = codec.encode_message(info_combo)
                
                # Ввод количества ошибок
                while True:
                    try:
                        m_input = input(f"\nВведите количество ошибок для внесения (0 ≤ m ≤ {s}): ").strip()
                        m = int(m_input)
                        
                        if m < 0:
                            print(f"Ошибка: количество ошибок не может быть отрицательным")
                            continue
                            
                        if m > s:
                            print(f"Ошибка: код может исправлять максимум {s} ошибок")
                            continue
                            
                        break
                    except ValueError:
                        print("Ошибка: введите целое число")
                
                if m > 0:
                    # Ввод позиций ошибок
                    print(f"\nВведите {m} позиций для ошибок (от 0 до {len(encoded)-1}):")
                    error_positions = []
                    
                    for i in range(m):
                        while True:
                            try:
                                pos_input = input(f"  Позиция {i+1}: ").strip()
                                pos = int(pos_input)
                                
                                if pos < 0 or pos >= len(encoded):
                                    print(f"    Ошибка: позиция должна быть от 0 до {len(encoded)-1}")
                                    continue
                                    
                                if pos in error_positions:
                                    print("    Ошибка: эта позиция уже выбрана")
                                    continue
                                    
                                error_positions.append(pos)
                                break
                            except ValueError:
                                print("    Ошибка: введите целое число")
                    
                    print("\n" + "=" * 60)
                    print("ВНЕСЕНИЕ ОШИБОК")
                    print("=" * 60)
                    
                    # Вносим ошибки
                    corrupted = codec.introduce_errors(encoded, sorted(error_positions))
                    
                    print("\n" + "=" * 60)
                    print("ИСПРАВЛЕНИЕ ОШИБОК")
                    print("=" * 60)
                    
                    # Исправляем ошибки
                    corrected = codec.decode_and_correct(corrupted)
                    
                    print("\n" + "=" * 60)
                    print("РЕЗУЛЬТАТЫ")
                    print("=" * 60)
                    print(f"Исходная комбинация:        {info_combo}")
                    print(f"Закодированная комбинация:  {encoded}")
                    print(f"Комбинация с ошибками:      {corrupted}")
                    print(f"Исправленная комбинация:    {corrected}")
                    
                    if encoded == corrected:
                        print("\n✓ Все ошибки успешно исправлены!")
                    else:
                        print("\n✗ Ошибки не были исправлены")
                        
                else:
                    print("\nОшибки не вносятся (m = 0)")
                    print(f"Кодовая комбинация: {encoded}")
                
            except ValueError as e:
                print(f"\nОшибка: {e}")
            except Exception as e:
                print(f"\nНеожиданная ошибка: {e}")
        
        elif choice == '2':
            print("\nВыход из приложения...")
            break
        
        else:
            print("\nНеверный выбор. Пожалуйста, выберите 1 или 2.")
        
        input("\nНажмите Enter чтобы продолжить...")


if __name__ == "__main__":
    main()