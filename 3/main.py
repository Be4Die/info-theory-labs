import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from collections import Counter, defaultdict
import math

class Node:
    def __init__(self, char, freq, index):
        self.char = char
        self.freq = freq
        self.index = index
        self.left = None
        self.right = None
        self.code = ''
        self.descendant_count = 0  # Количество потомков

class HuffmanCoding:
    def __init__(self):
        self.codes = {}
    
    def count_descendants(self, node):
        if node is None:
            return 0
        if node.char is not None:
            node.descendant_count = 0
            return 1
        
        left_count = self.count_descendants(node.left)
        right_count = self.count_descendants(node.right)
        node.descendant_count = left_count + right_count
        return node.descendant_count
    
    def get_node_priority(self, node):
        """Определяет приоритет узла для сравнения"""
        # Основной критерий - частота (меньшая частота имеет высший приоритет)
        # При одинаковой частоте - узел с большим количеством потомков имеет высший приоритет
        # При одинаковом количестве потомков - узел с большим индексом (позже в таблице) имеет высший приоритет
        return (node.freq, -node.descendant_count, -node.index)
    
    def build_tree(self, frequencies):
        # Создаем узлы с сохранением индекса из исходного списка
        nodes = []
        for i, (char, freq) in enumerate(frequencies):
            node = Node(char, freq, i)
            nodes.append(node)
        
        # Строим дерево снизу вверх
        step = 0
        while len(nodes) > 1:
            # Пересчитываем количество потомков для всех узлов
            for node in nodes:
                self.count_descendants(node)
            
            # Сортируем узлы по приоритету
            nodes.sort(key=self.get_node_priority)
            
            # Берем два узла с наивысшим приоритетом (наименьшая частота)
            left = nodes.pop(0)
            right = nodes.pop(0)
            
            # Создаем новый узел
            # Индекс нового узла = минимальный из индексов детей
            # Это сохраняет приоритет узлов, которые были раньше в таблице
            merged = Node(None, left.freq + right.freq, min(left.index, right.index))
            merged.left = left
            merged.right = right
            
            # Добавляем новый узел обратно в список
            nodes.append(merged)
            step += 1
        
        return nodes[0] if nodes else None
    
    def generate_codes(self, node, current_code=''):
        if node is None:
            return
        
        if node.char is not None:
            self.codes[node.char] = current_code
            return
        
        self.generate_codes(node.left, current_code + '0')
        self.generate_codes(node.right, current_code + '1')

class ShannonFanoCoding:
    def __init__(self):
        self.codes = {}
        self.steps = []
    
    def build_tree(self, frequencies):
        sorted_freq = self.custom_sort(frequencies)
        self._generate_codes_recursive(sorted_freq, '')
        return self.codes
    
    def custom_sort(self, frequencies):
        freq_dict = dict(frequencies)
        char_order = {}
        order = 0
        for char, _ in frequencies:
            if char not in char_order:
                char_order[char] = order
                order += 1
        
        return sorted(frequencies, key=lambda x: (-x[1], char_order[x[0]]))
    
    def _generate_codes_recursive(self, symbols, current_code):
        if len(symbols) == 1:
            self.codes[symbols[0][0]] = current_code
            return
        
        total_freq = sum(freq for _, freq in symbols)
        
        # Ищем оптимальное разделение, где первая группа <= второй
        best_diff = float('inf')
        best_index = 0
        current_freq = 0
        
        for i in range(len(symbols)):
            current_freq += symbols[i][1]
            # Первая группа должна быть <= второй
            if current_freq <= total_freq - current_freq:
                diff = abs(2 * current_freq - total_freq)
                if diff < best_diff:
                    best_diff = diff
                    best_index = i + 1
            else:
                break
        
        if best_index == 0:
            best_index = 1
        
        group1 = symbols[:best_index]
        group2 = symbols[best_index:]
        
        sum1 = sum(freq for _, freq in group1)
        sum2 = sum(freq for _, freq in group2)
        
        self.steps.append({
            'group1': group1.copy(),
            'group2': group2.copy(),
            'sum1': sum1,
            'sum2': sum2,
            'code1': current_code + '0',
            'code2': current_code + '1'
        })
        
        self._generate_codes_recursive(group1, current_code + '0')
        self._generate_codes_recursive(group2, current_code + '1')

class CodingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Кодирование Шеннона-Фано и Хаффмана")
        self.root.geometry("1400x900")
        
        self.message = ""
        self.frequencies = []
        self.shannon_fano_codes = {}
        self.huffman_codes = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        # Основной фрейм с прокруткой
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Создаем холст и скроллбар для основного окна
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Ввод сообщения
        input_frame = ttk.LabelFrame(scrollable_frame, text="Ввод сообщения", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.text_input = tk.Text(input_frame, height=5, width=100)
        self.text_input.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Кнопки
        ttk.Button(input_frame, text="Загрузить из файла", 
                  command=self.load_from_file).grid(row=1, column=0, padx=(0, 10))
        ttk.Button(input_frame, text="Анализировать", 
                  command=self.analyze).grid(row=1, column=1)
        
        # Ноутбук для разделения на вкладки
        notebook = ttk.Notebook(scrollable_frame)
        notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Вкладка частот и кодов
        freq_frame = ttk.Frame(notebook, padding="10")
        notebook.add(freq_frame, text="Символы и коды")
        
        # Таблица символов, частот и кодов
        freq_codes_frame = ttk.LabelFrame(freq_frame, text="Символы, частоты и коды")
        freq_codes_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.freq_tree = ttk.Treeview(freq_codes_frame, 
                                     columns=('char', 'freq', 'percent', 'sf_code', 'huff_code'),
                                     show='headings', height=20)
        
        self.freq_tree.heading('char', text='Символ')
        self.freq_tree.heading('freq', text='Частота')
        self.freq_tree.heading('percent', text='Вероятность (%)')
        self.freq_tree.heading('sf_code', text='Код Шеннона-Фано')
        self.freq_tree.heading('huff_code', text='Код Хаффмана')
        
        self.freq_tree.column('char', width=80)
        self.freq_tree.column('freq', width=80)
        self.freq_tree.column('percent', width=100)
        self.freq_tree.column('sf_code', width=120)
        self.freq_tree.column('huff_code', width=120)
        
        freq_scrollbar = ttk.Scrollbar(freq_codes_frame, orient=tk.VERTICAL, command=self.freq_tree.yview)
        self.freq_tree.configure(yscrollcommand=freq_scrollbar.set)
        
        self.freq_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        freq_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Вкладка Шеннона-Фано
        sf_frame = ttk.Frame(notebook, padding="10")
        notebook.add(sf_frame, text="Шеннон-Фано")
        
        # Таблица шагов Шеннона-Фано
        sf_table_frame = ttk.LabelFrame(sf_frame, text="Процесс построения кода Шеннона-Фано")
        sf_table_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.sf_tree = ttk.Treeview(sf_table_frame, 
                                   columns=('step', 'group1', 'sum1', 'group2', 'sum2', 'codes'),
                                   show='headings', height=20)
        
        self.sf_tree.heading('step', text='Шаг')
        self.sf_tree.heading('group1', text='Группа 1 (0)')
        self.sf_tree.heading('sum1', text='Сумма 1')
        self.sf_tree.heading('group2', text='Группа 2 (1)')
        self.sf_tree.heading('sum2', text='Сумма 2')
        self.sf_tree.heading('codes', text='Коды')
        
        self.sf_tree.column('step', width=60)
        self.sf_tree.column('group1', width=200)
        self.sf_tree.column('sum1', width=80)
        self.sf_tree.column('group2', width=200)
        self.sf_tree.column('sum2', width=80)
        self.sf_tree.column('codes', width=200)
        
        sf_scrollbar = ttk.Scrollbar(sf_table_frame, orient=tk.VERTICAL, command=self.sf_tree.yview)
        self.sf_tree.configure(yscrollcommand=sf_scrollbar.set)
        
        self.sf_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        sf_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Вкладка Хаффмана
        huff_frame = ttk.Frame(notebook, padding="10")
        notebook.add(huff_frame, text="Хаффман")
        
        # Дерево Хаффмана
        huff_tree_frame = ttk.LabelFrame(huff_frame, text="Дерево Хаффмана")
        huff_tree_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Создаем фрейм с прокруткой для дерева Хаффмана
        huff_canvas_frame = ttk.Frame(huff_tree_frame)
        huff_canvas_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.huff_tree_canvas = tk.Canvas(huff_canvas_frame, width=1000, height=500, bg='white')
        huff_hscrollbar = ttk.Scrollbar(huff_canvas_frame, orient=tk.HORIZONTAL, command=self.huff_tree_canvas.xview)
        huff_vscrollbar = ttk.Scrollbar(huff_canvas_frame, orient=tk.VERTICAL, command=self.huff_tree_canvas.yview)
        
        self.huff_tree_canvas.configure(xscrollcommand=huff_hscrollbar.set, yscrollcommand=huff_vscrollbar.set)
        
        self.huff_tree_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        huff_vscrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        huff_hscrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Результаты кодирования
        results_frame = ttk.LabelFrame(scrollable_frame, text="Результаты кодирования", padding="10")
        results_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(results_frame, text="Исходное сообщение:").grid(row=0, column=0, sticky=tk.W)
        self.original_message = tk.Text(results_frame, height=3, width=100)
        self.original_message.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(results_frame, text="Закодированное Шенноном-Фано:").grid(row=2, column=0, sticky=tk.W)
        self.sf_encoded = tk.Text(results_frame, height=3, width=100)
        self.sf_encoded.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(results_frame, text="Закодированное Хаффманом:").grid(row=4, column=0, sticky=tk.W)
        self.huff_encoded = tk.Text(results_frame, height=3, width=100)
        self.huff_encoded.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Статистика
        stats_frame = ttk.LabelFrame(scrollable_frame, text="Статистика", padding="10")
        stats_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.stats_text = tk.Text(stats_frame, height=4, width=100)
        self.stats_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Настройка весов для растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        scrollable_frame.columnconfigure(0, weight=1)
        
        freq_frame.columnconfigure(0, weight=1)
        freq_frame.rowconfigure(0, weight=1)
        freq_codes_frame.columnconfigure(0, weight=1)
        freq_codes_frame.rowconfigure(0, weight=1)
        
        sf_frame.columnconfigure(0, weight=1)
        sf_frame.rowconfigure(0, weight=1)
        sf_table_frame.columnconfigure(0, weight=1)
        sf_table_frame.rowconfigure(0, weight=1)
        
        huff_frame.columnconfigure(0, weight=1)
        huff_frame.rowconfigure(0, weight=1)
        huff_tree_frame.columnconfigure(0, weight=1)
        huff_tree_frame.rowconfigure(0, weight=1)
        huff_canvas_frame.columnconfigure(0, weight=1)
        huff_canvas_frame.rowconfigure(0, weight=1)
        
        results_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(0, weight=1)
    
    def load_from_file(self):
        filename = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=(("Текстовые файлы", "*.txt"), ("Все файлы", "*.*"))
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_input.delete('1.0', tk.END)
                    self.text_input.insert('1.0', content)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {str(e)}")
    
    def analyze(self):
        self.message = self.text_input.get('1.0', tk.END).strip()
        
        if not self.message:
            messagebox.showwarning("Предупреждение", "Введите сообщение для анализа")
            return
        
        # Очистка предыдущих данных
        for tree in [self.freq_tree, self.sf_tree]:
            for item in tree.get_children():
                tree.delete(item)
        
        self.huff_tree_canvas.delete("all")
        self.original_message.delete('1.0', tk.END)
        self.sf_encoded.delete('1.0', tk.END)
        self.huff_encoded.delete('1.0', tk.END)
        self.stats_text.delete('1.0', tk.END)
        
        # Расчет частот
        self.calculate_frequencies()
        
        # Построение кодов
        self.build_shannon_fano()
        self.build_huffman()
        
        # Отображение результатов
        self.show_results()
    
    def calculate_frequencies(self):
        counter = Counter(self.message)
        total_chars = len(self.message)
        
        # Создаем список символов с учетом порядка первого вхождения
        char_order = {}
        ordered_chars = []
        for char in self.message:
            if char not in char_order:
                char_order[char] = len(ordered_chars)
                ordered_chars.append(char)
        
        # Сортируем по убыванию частоты, при равенстве - по порядку первого вхождения
        self.frequencies = sorted([(char, count) for char, count in counter.items()],
                                 key=lambda x: (-x[1], char_order[x[0]]))
    
    def build_shannon_fano(self):
        sf = ShannonFanoCoding()
        self.shannon_fano_codes = sf.build_tree(self.frequencies)
        
        # Отображаем шаги построения
        for i, step in enumerate(sf.steps, 1):
            group1_str = ', '.join([f"'{repr(char)[1:-1]}':{freq}" for char, freq in step['group1']])
            group2_str = ', '.join([f"'{repr(char)[1:-1]}':{freq}" for char, freq in step['group2']])
            
            self.sf_tree.insert('', tk.END, values=(
                i, group1_str, step['sum1'], group2_str, step['sum2'],
                f"Группа1: {step['code1']}, Группа2: {step['code2']}"
            ))
    
    def build_huffman(self):
        huffman = HuffmanCoding()
        root = huffman.build_tree(self.frequencies)
        huffman.generate_codes(root)
        self.huffman_codes = huffman.codes
        
        # Визуализируем дерево
        self.draw_huffman_tree(root)
    
    def draw_huffman_tree(self, root):
        if not root:
            return
        
        canvas = self.huff_tree_canvas
        canvas.delete("all")
        
        # Рекурсивная функция для расчета позиций
        def calculate_positions(node, x, y, dx, level=0, positions=None):
            if positions is None:
                positions = {}
            
            if node is None:
                return positions
            
            positions[node] = (x, y)
            
            if node.left:
                positions = calculate_positions(node.left, x - dx, y + 80, dx/1.8, level+1, positions)
            
            if node.right:
                positions = calculate_positions(node.right, x + dx, y + 80, dx/1.8, level+1, positions)
            
            return positions
        
        # Рекурсивная функция для рисования дерева
        def draw_tree(node, positions):
            if node is None:
                return
            
            x, y = positions[node]
            
            # Рисуем узел
            if node.char is not None:
                label = f"'{repr(node.char)[1:-1]}'\n{node.freq}\n{self.huffman_codes[node.char]}"
                color = "lightblue"
            else:
                label = f"{node.freq}\nпотомков: {node.descendant_count}"
                color = "lightgreen"
            
            canvas.create_oval(x-30, y-20, x+30, y+20, fill=color, outline="black")
            canvas.create_text(x, y, text=label, font=("Arial", 8))
            
            # Рисуем связи с детьми
            if node.left:
                x_left, y_left = positions[node.left]
                canvas.create_line(x, y+20, x_left, y_left-20, arrow=tk.LAST, dash=(4,2))
                canvas.create_text((x + x_left)//2, (y + y_left)//2, 
                                 text="0", font=("Arial", 10, "bold"))
                draw_tree(node.left, positions)
            
            if node.right:
                x_right, y_right = positions[node.right]
                canvas.create_line(x, y+20, x_right, y_right-20, arrow=tk.LAST)
                canvas.create_text((x + x_right)//2, (y + y_right)//2, 
                                 text="1", font=("Arial", 10, "bold"))
                draw_tree(node.right, positions)
        
        # Рассчитываем позиции и рисуем дерево
        positions = calculate_positions(root, 500, 50, 300)
        draw_tree(root, positions)
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    def show_results(self):
        # Исходное сообщение
        self.original_message.insert('1.0', self.message)
        
        # Кодирование Шеннона-Фано
        sf_encoded = ''.join(self.shannon_fano_codes[char] for char in self.message)
        self.sf_encoded.insert('1.0', sf_encoded)
        
        # Кодирование Хаффмана
        huff_encoded = ''.join(self.huffman_codes[char] for char in self.message)
        self.huff_encoded.insert('1.0', huff_encoded)
        
        # Заполняем таблицу символов, частот и кодов в правильном порядке
        total_chars = len(self.message)
        for char, freq in self.frequencies:
            percent = (freq / total_chars) * 100
            sf_code = self.shannon_fano_codes.get(char, '')
            huff_code = self.huffman_codes.get(char, '')
            
            self.freq_tree.insert('', tk.END, values=(
                repr(char)[1:-1], freq, f"{percent:.2f}%", sf_code, huff_code
            ))
        
        # Статистика
        sf_length = len(sf_encoded)
        huff_length = len(huff_encoded)
        original_bits = len(self.message) * 8  # Предполагаем 8 бит на символ
        
        compression_sf = (1 - sf_length / original_bits) * 100
        compression_huff = (1 - huff_length / original_bits) * 100
        
        stats = f"Статистика:\n"
        stats += f"Исходный размер: {original_bits} бит\n"
        stats += f"Размер после Шеннона-Фано: {sf_length} бит (сжатие: {compression_sf:.2f}%)\n"
        stats += f"Размер после Хаффмана: {huff_length} бит (сжатие: {compression_huff:.2f}%)\n"
        stats += f"Средняя длина кода Шеннона-Фано: {sf_length/len(self.message):.2f} бит/символ\n"
        stats += f"Средняя длина кода Хаффмана: {huff_length/len(self.message):.2f} бит/символ"
        
        self.stats_text.insert('1.0', stats)

def main():
    root = tk.Tk()
    app = CodingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()