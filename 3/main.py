import math
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from collections import Counter


class Node:
    def __init__(self, symbol=None, probability=0):
        self.symbol = symbol
        self.probability = probability
        self.left = None
        self.right = None
        self.code = ""
        self.parent = None  # Добавляем ссылку на родительский узел


def calculate_entropy(probabilities):
    entropy = 0
    for p in probabilities:
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def shannon_fano(symbols_prob):
    def split_list(lst):
        if len(lst) == 1:
            return lst, []

        total = sum(p for _, p in lst)
        half = total / 2
        current_sum = 0
        split_index = 0

        for i, (_, p) in enumerate(lst):
            current_sum += p
            if current_sum >= half:
                split_index = i + 1
                break

        return lst[:split_index], lst[split_index:]

    def assign_codes(lst, code=""):
        if len(lst) == 1:
            symbol, prob = lst[0]
            codes[symbol] = code
            return

        left, right = split_list(lst)
        assign_codes(left, code + "0")
        assign_codes(right, code + "1")

    symbols_sorted = sorted(symbols_prob.items(), key=lambda x: x[1], reverse=True)
    codes = {}
    assign_codes(symbols_sorted)
    return codes


def build_huffman_tree(symbols_prob):
    # Создаем узлы и сортируем по убыванию вероятности
    nodes = [Node(symbol, prob) for symbol, prob in symbols_prob.items()]
    nodes.sort(key=lambda x: -x.probability)

    # Строим дерево согласно схеме из примера
    while len(nodes) > 1:
        # Берем два узла с наименьшими вероятностями (последние в отсортированном списке)
        right = nodes.pop()
        left = nodes.pop()

        # Создаем родительский узел
        parent = Node(probability=left.probability + right.probability)
        parent.left = left
        parent.right = right
        left.parent = parent
        right.parent = parent

        # Вставляем обратно в отсортированный список
        nodes.append(parent)
        nodes.sort(key=lambda x: -x.probability)

    return nodes[0] if nodes else None


def assign_huffman_codes(node, code="", codes=None):
    if codes is None:
        codes = {}

    if node is None:
        return codes

    node.code = code

    if node.symbol is not None:
        codes[node.symbol] = code

    # Левые ребра помечаем 1, правые - 0 (согласно примеру)
    assign_huffman_codes(node.left, code + "1", codes)
    assign_huffman_codes(node.right, code + "0", codes)

    return codes


def calculate_average_code_length(codes, probabilities):
    total = 0
    for symbol, code in codes.items():
        total += len(code) * probabilities.get(symbol, 0)
    return total


class CodingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа №3 - Оптимальное кодирование")
        self.root.geometry("1400x900")

        # Увеличиваем масштаб для высокого разрешения
        self.setup_hidpi()
        self.setup_ui()
        self.message = ""
        self.symbols_prob = {}
        self.codes_shannon = {}
        self.codes_huffman = {}
        self.huffman_tree = None

    def setup_hidpi(self):
        """Настройка для HiDPI дисплеев"""
        try:
            from ctypes import windll

            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass

    def setup_ui(self):
        # Увеличиваем размер шрифтов для высокого разрешения
        style = ttk.Style()
        style.configure("Large.TFrame", padding=20)
        style.configure("Large.TLabel", font=("Arial", 18))  # Увеличили шрифт
        style.configure("Large.TButton", font=("Arial", 18))  # Увеличили шрифт
        style.configure("TLabelframe", font=("Arial", 18, "bold"))  # Увеличили шрифт
        style.configure(
            "TLabelframe.Label", font=("Arial", 18, "bold")
        )  # Увеличили шрифт
        style.configure("TNotebook", font=("Arial", 16))  # Увеличили шрифт вкладок
        style.configure(
            "TNotebook.Tab", font=("Arial", 16, "bold")
        )  # Увеличили шрифт вкладок

        # Основные фреймы
        main_frame = ttk.Frame(self.root, style="Large.TFrame")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Ввод данных
        input_frame = ttk.LabelFrame(main_frame, text="Ввод сообщения", padding="20")
        input_frame.grid(
            row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20)
        )

        # Увеличиваем высоту текстового поля
        self.text_input = tk.Text(
            input_frame, height=8, width=100, font=("Arial", 18)
        )  # Увеличили шрифт
        self.text_input.grid(
            row=0, column=0, columnspan=2, pady=(0, 20), sticky=(tk.W, tk.E)
        )

        ttk.Button(
            input_frame,
            text="Анализировать сообщение",
            command=self.analyze_message,
            style="Large.TButton",
        ).grid(row=1, column=0, pady=15, padx=(0, 15))
        ttk.Button(
            input_frame,
            text="Загрузить из файла",
            command=self.load_from_file,
            style="Large.TButton",
        ).grid(row=1, column=1, pady=15)

        # Статистика и визуализация
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(
            row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S)
        )

        # Статистика
        stats_frame = ttk.LabelFrame(
            content_frame, text="Статистика сообщения", padding="20"
        )
        stats_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 20))

        # Увеличиваем шрифт статистики
        self.stats_text = tk.Text(
            stats_frame,
            height=25,
            width=70,
            font=("Consolas", 18),  # Увеличили шрифт
        )
        stats_scrollbar = ttk.Scrollbar(
            stats_frame, orient="vertical", command=self.stats_text.yview
        )
        self.stats_text.configure(yscrollcommand=stats_scrollbar.set)
        self.stats_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        stats_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Визуализация
        viz_frame = ttk.LabelFrame(
            content_frame, text="Визуализация алгоритмов кодирования", padding="20"
        )
        viz_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Notebook для переключения между методами
        self.notebook = ttk.Notebook(viz_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Фрейм для Шеннона-Фано
        self.shannon_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.shannon_frame, text="Шеннон-Фано")

        self.shannon_canvas = tk.Canvas(
            self.shannon_frame, width=600, height=500, bg="white", highlightthickness=0
        )
        shannon_scrollbar_v = ttk.Scrollbar(
            self.shannon_frame, orient="vertical", command=self.shannon_canvas.yview
        )
        shannon_scrollbar_h = ttk.Scrollbar(
            self.shannon_frame, orient="horizontal", command=self.shannon_canvas.xview
        )
        self.shannon_canvas.configure(
            yscrollcommand=shannon_scrollbar_v.set,
            xscrollcommand=shannon_scrollbar_h.set,
        )

        self.shannon_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        shannon_scrollbar_v.grid(row=0, column=1, sticky=(tk.N, tk.S))
        shannon_scrollbar_h.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # Фрейм для Хаффмана
        self.huffman_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.huffman_frame, text="Хаффман")

        self.huffman_canvas = tk.Canvas(
            self.huffman_frame, width=600, height=500, bg="white", highlightthickness=0
        )
        huffman_scrollbar_v = ttk.Scrollbar(
            self.huffman_frame, orient="vertical", command=self.huffman_canvas.yview
        )
        huffman_scrollbar_h = ttk.Scrollbar(
            self.huffman_frame, orient="horizontal", command=self.huffman_canvas.xview
        )
        self.huffman_canvas.configure(
            yscrollcommand=huffman_scrollbar_v.set,
            xscrollcommand=huffman_scrollbar_h.set,
        )

        self.huffman_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        huffman_scrollbar_v.grid(row=0, column=1, sticky=(tk.N, tk.S))
        huffman_scrollbar_h.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # Кодирование сообщения
        encode_frame = ttk.LabelFrame(
            main_frame, text="Кодирование произвольного сообщения", padding="20"
        )
        encode_frame.grid(
            row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0)
        )

        ttk.Label(
            encode_frame, text="Сообщение для кодирования:", style="Large.TLabel"
        ).grid(row=0, column=0, sticky=tk.W)
        self.encode_input = ttk.Entry(
            encode_frame, width=60, font=("Arial", 18)
        )  # Увеличили шрифт
        self.encode_input.grid(row=0, column=1, padx=(15, 15), sticky=(tk.W, tk.E))

        ttk.Button(
            encode_frame,
            text="Закодировать",
            command=self.encode_message,
            style="Large.TButton",
        ).grid(row=0, column=2)

        ttk.Label(
            encode_frame, text="Результаты кодирования:", style="Large.TLabel"
        ).grid(row=1, column=0, sticky=tk.W, pady=(20, 0))
        self.result_text = tk.Text(
            encode_frame,
            height=5,
            width=100,
            font=("Consolas", 18),  # Увеличили шрифт
        )
        self.result_text.grid(
            row=2, column=0, columnspan=3, pady=(10, 0), sticky=(tk.W, tk.E)
        )

        # Настройка весов для растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.rowconfigure(0, weight=1)
        viz_frame.columnconfigure(0, weight=1)
        viz_frame.rowconfigure(0, weight=1)
        self.shannon_frame.columnconfigure(0, weight=1)
        self.shannon_frame.rowconfigure(0, weight=1)
        self.huffman_frame.columnconfigure(0, weight=1)
        self.huffman_frame.rowconfigure(0, weight=1)
        encode_frame.columnconfigure(1, weight=1)

    def load_from_file(self):
        try:
            filename = filedialog.askopenfilename(
                title="Выберите файл",
                filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")],
            )
            if filename:
                with open(filename, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.text_input.delete(1.0, tk.END)
                    self.text_input.insert(1.0, content)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {str(e)}")

    def analyze_message(self):
        self.message = self.text_input.get(1.0, tk.END).strip()

        if not self.message:
            messagebox.showwarning("Предупреждение", "Введите сообщение для анализа")
            return

        try:
            # Статистика одиночных символов
            total_chars = len(self.message)
            char_counter = Counter(self.message)

            self.symbols_prob = {}
            for char, count in char_counter.items():
                self.symbols_prob[char] = count / total_chars

            # Сортировка по убыванию вероятности
            sorted_symbols = sorted(
                self.symbols_prob.items(), key=lambda x: x[1], reverse=True
            )

            # Вычисление энтропии
            probabilities = [prob for _, prob in sorted_symbols]
            H_X = calculate_entropy(probabilities)

            # Кодирование Шеннона-Фано
            self.codes_shannon = shannon_fano(self.symbols_prob)
            avg_length_shannon = calculate_average_code_length(
                self.codes_shannon, self.symbols_prob
            )
            efficiency_shannon = (
                H_X / avg_length_shannon if avg_length_shannon > 0 else 0
            )

            # Кодирование Хаффмана
            self.huffman_tree = build_huffman_tree(self.symbols_prob)
            self.codes_huffman = assign_huffman_codes(self.huffman_tree)
            avg_length_huffman = calculate_average_code_length(
                self.codes_huffman, self.symbols_prob
            )
            efficiency_huffman = (
                H_X / avg_length_huffman if avg_length_huffman > 0 else 0
            )

            # Вывод статистики
            self.display_statistics(
                sorted_symbols,
                H_X,
                avg_length_shannon,
                efficiency_shannon,
                avg_length_huffman,
                efficiency_huffman,
            )

            # Визуализация
            self.visualize_shannon_fano()
            self.visualize_huffman()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при анализе: {str(e)}")

    def display_statistics(
        self, sorted_symbols, H_X, avg_shannon, eff_shannon, avg_huffman, eff_huffman
    ):
        self.stats_text.delete(1.0, tk.END)

        # Основная информация
        self.stats_text.insert(
            tk.END, f"Длина сообщения: {len(self.message)} символов\n"
        )
        self.stats_text.insert(tk.END, f"Различных символов: {len(sorted_symbols)}\n")
        self.stats_text.insert(tk.END, f"Энтропия H(X): {H_X:.4f} бит\n\n")

        # Статистика символов
        self.stats_text.insert(tk.END, "СТАТИСТИКА СИМВОЛОВ:\n")
        self.stats_text.insert(tk.END, "=" * 70 + "\n")
        self.stats_text.insert(
            tk.END, "Символ  Частота  Вероятность  Код Шеннона-Фано  Код Хаффмана\n"
        )
        self.stats_text.insert(tk.END, "=" * 70 + "\n")

        for symbol, prob in sorted_symbols:
            count = int(prob * len(self.message))
            shannon_code = self.codes_shannon.get(symbol, "")
            huffman_code = self.codes_huffman.get(symbol, "")
            self.stats_text.insert(
                tk.END,
                f"  '{symbol}'   {count:<6}   {prob:<10.4f}   {shannon_code:<15}   {huffman_code}\n",
            )

        # Энтропия и эффективность
        self.stats_text.insert(tk.END, "\nЭФФЕКТИВНОСТЬ КОДИРОВАНИЯ:\n")
        self.stats_text.insert(tk.END, "=" * 70 + "\n")
        self.stats_text.insert(
            tk.END, f"Средняя длина кода (Шеннон-Фано): {avg_shannon:.4f} бит/символ\n"
        )
        self.stats_text.insert(
            tk.END, f"Эффективность (Шеннон-Фано): {eff_shannon:.4f}\n"
        )
        self.stats_text.insert(
            tk.END, f"Средняя длина кода (Хаффман): {avg_huffman:.4f} бит/символ\n"
        )
        self.stats_text.insert(tk.END, f"Эффективность (Хаффман): {eff_huffman:.4f}\n")

    def visualize_shannon_fano(self):
        self.shannon_canvas.delete("all")

        if not self.codes_shannon:
            return

        # Увеличиваем размеры для лучшей читаемости на высоком разрешении
        node_radius = 45  # Увеличили радиус
        level_height = 120  # Увеличили высоту уровня
        font_size = 14  # Увеличили шрифт

        # Создаем дерево из кодов
        root = Node()
        nodes = {"": root}

        # Строим дерево на основе кодов
        for symbol, code in self.codes_shannon.items():
            current_node = root
            for bit in code:
                if bit == "0":
                    if current_node.left is None:
                        current_node.left = Node()
                        current_node.left.parent = current_node
                        nodes[code[: len(current_node.code) + 1]] = current_node.left
                    current_node = current_node.left
                else:
                    if current_node.right is None:
                        current_node.right = Node()
                        current_node.right.parent = current_node
                        nodes[code[: len(current_node.code) + 1]] = current_node.right
                    current_node = current_node.right
                current_node.code = code[: len(current_node.code) + 1]
            current_node.symbol = symbol
            current_node.probability = self.symbols_prob.get(symbol, 0)

        # Рисуем дерево
        self.draw_tree(
            self.shannon_canvas,
            root,
            "Шеннон-Фано",
            node_radius,
            level_height,
            font_size,
            "shannon",
        )

        # Устанавливаем область прокрутки
        self.shannon_canvas.configure(scrollregion=self.shannon_canvas.bbox("all"))

    def visualize_huffman(self):
        self.huffman_canvas.delete("all")

        if not self.huffman_tree:
            return

        # Увеличиваем размеры для лучшей читаемости на высоком разрешении
        node_radius = 45  # Увеличили радиус
        level_height = 120  # Увеличили высоту уровня
        font_size = 14  # Увеличили шрифт

        self.draw_tree(
            self.huffman_canvas,
            self.huffman_tree,
            "Хаффман",
            node_radius,
            level_height,
            font_size,
            "huffman",
        )

        # Устанавливаем область прокрутки
        self.huffman_canvas.configure(scrollregion=self.huffman_canvas.bbox("all"))

    def draw_tree(
        self,
        canvas,
        root,
        title,
        node_radius,
        level_height,
        font_size,
        method="shannon",
    ):
        # Рассчитываем позиции узлов
        positions = {}
        levels = {}

        def calculate_positions(node, level=0, pos=0):
            if node is None:
                return pos

            if level not in levels:
                levels[level] = []
            levels[level].append(node)

            left_pos = calculate_positions(node.left, level + 1, pos)
            current_pos = left_pos + 1
            right_pos = calculate_positions(node.right, level + 1, current_pos)

            positions[node] = (current_pos, level)
            return right_pos

        total_width = calculate_positions(root)

        if not levels:
            return

        max_level = max(levels.keys())
        start_x = 100
        start_y = 80

        # Определяем метки для ребер в зависимости от метода
        if method == "huffman":
            left_label = "1"
            right_label = "0"
        else:  # shannon
            left_label = "0"
            right_label = "1"

        # Рисуем узлы и связи
        for node, (pos, level) in positions.items():
            x = start_x + (pos / total_width) * 1000
            y = start_y + level * level_height

            # Рисуем связи с детьми
            if node.left and node.left in positions:
                left_x, left_y = positions[node.left]
                left_x = start_x + (left_x / total_width) * 1000
                left_y = start_y + left_y * level_height
                canvas.create_line(
                    x,
                    y + node_radius,
                    left_x,
                    left_y - node_radius,
                    width=4,  # Увеличили толщину линии
                    fill="black",
                    arrow=tk.LAST,
                    arrowshape=(20, 25, 8),  # Увеличили размер стрелки
                )
                canvas.create_text(
                    (x + left_x) / 2,
                    (y + left_y) / 2,
                    text=left_label,
                    font=("Arial", font_size, "bold"),
                    fill="red",
                )

            if node.right and node.right in positions:
                right_x, right_y = positions[node.right]
                right_x = start_x + (right_x / total_width) * 1000
                right_y = start_y + right_y * level_height
                canvas.create_line(
                    x,
                    y + node_radius,
                    right_x,
                    right_y - node_radius,
                    width=4,  # Увеличили толщину линии
                    fill="black",
                    arrow=tk.LAST,
                    arrowshape=(20, 25, 8),  # Увеличили размер стрелки
                )
                canvas.create_text(
                    (x + right_x) / 2,
                    (y + right_y) / 2,
                    text=right_label,
                    font=("Arial", font_size, "bold"),
                    fill="red",
                )

            # Рисуем узел
            color = "lightgreen" if node.symbol else "lightblue"
            canvas.create_oval(
                x - node_radius,
                y - node_radius,
                x + node_radius,
                y + node_radius,
                fill=color,
                outline="black",
                width=3,  # Увеличили толщину обводки
            )

            # Текст в узле
            if node.symbol:
                text = f"'{node.symbol}'\n{node.code}"
                canvas.create_text(
                    x,
                    y,
                    text=text,
                    font=("Arial", font_size - 1),
                    justify=tk.CENTER,
                    width=node_radius * 1.8,
                )
            else:
                text = f"p={node.probability:.3f}"
                canvas.create_text(
                    x, y, text=text, font=("Arial", font_size), justify=tk.CENTER
                )

        # Заголовок с увеличенным шрифтом
        canvas.create_text(
            400,
            30,
            text=f"Дерево кодирования - {title}",
            font=("Arial", 18, "bold"),  # Увеличили шрифт
        )

    def encode_message(self):
        message = self.encode_input.get().strip()

        if not message:
            messagebox.showwarning(
                "Предупреждение", "Введите сообщение для кодирования"
            )
            return

        if not self.codes_shannon or not self.codes_huffman:
            messagebox.showwarning(
                "Предупреждение", "Сначала выполните анализ сообщения"
            )
            return

        # Кодируем сообщение
        encoded_shannon = ""
        encoded_huffman = ""

        try:
            for char in message:
                if char in self.codes_shannon:
                    encoded_shannon += self.codes_shannon[char]
                else:
                    encoded_shannon += f"[{char}?]"

                if char in self.codes_huffman:
                    encoded_huffman += self.codes_huffman[char]
                else:
                    encoded_huffman += f"[{char}?]"

            # Выводим результат
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Исходное сообщение: {message}\n\n")
            self.result_text.insert(
                tk.END,
                f"Код Шеннона-Фано ({len(encoded_shannon)} бит):\n{encoded_shannon}\n\n",
            )
            self.result_text.insert(
                tk.END, f"Код Хаффмана ({len(encoded_huffman)} бит):\n{encoded_huffman}"
            )

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при кодировании: {str(e)}")


def main():
    root = tk.Tk()
    app = CodingVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
