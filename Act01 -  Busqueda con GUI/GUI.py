import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Act01 -  Busqueda con GUI 
# Valentin Gallardo Jose Eduardo 
# Analisis de Algoritmos - seccion D01
# Comparador de Algoritmos de Búsqueda

class SearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Comparador de Algoritmos de Búsqueda")
        self.root.geometry("900x700")
        self.root.color = "#BBDCE5"        
        # Variables de estado
        self.current_list = None
        self.current_size = None
        self.results = {
            'linear': {'times': [], 'averages': {}},
            'binary': {'times': [], 'averages': {}}
        }
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure('TFrame', padding=5)
        self.style.configure('TButton', padding=5)
        self.style.configure('TLabel', padding=5)
        
        # Crear widgets
        self.create_widgets()
        
        # Inicializar gráfica
        self.init_graph()
    
    def create_widgets(self):
        """Crea todos los widgets de la interfaz."""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame de controles superiores
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Frame de generación de datos (izquierda)
        data_frame = ttk.LabelFrame(top_frame, text="Generar Datos")
        data_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(data_frame, text="Tamaño de lista:").pack(side=tk.LEFT)
        self.size_combobox = ttk.Combobox(data_frame, 
                                         values=[100, 1000, 10000, 100000], 
                                         state="readonly")
        self.size_combobox.pack(side=tk.LEFT, padx=5)
        self.size_combobox.current(0)
        
        self.generate_btn = ttk.Button(data_frame, text="Generar", 
                                     command=self.generate_data)
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        # Frame de búsqueda (derecha)
        search_frame = ttk.LabelFrame(top_frame, text="Buscar Valor")
        search_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(search_frame, text="Valor:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=15)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        self.linear_btn = ttk.Button(search_frame, text="Búsqueda Lineal", 
                                   state=tk.DISABLED, 
                                   command=lambda: self.run_search('linear'))
        self.linear_btn.pack(side=tk.LEFT, padx=2)
        
        self.binary_btn = ttk.Button(search_frame, text="Búsqueda Binaria", 
                                  state=tk.DISABLED, 
                                  command=lambda: self.run_search('binary'))
        self.binary_btn.pack(side=tk.LEFT, padx=2)
        
        # Frame de resultados
        result_frame = ttk.LabelFrame(main_frame, text="Resultados")
        result_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.result_text = tk.Text(result_frame, height=6, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(result_frame, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Frame de gráfica
        graph_frame = ttk.LabelFrame(main_frame, text="Comparación de Tiempos (ms)")
        graph_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configurar figura de matplotlib
        self.fig, self.ax = plt.subplots(figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Frame de experimentos
        exp_frame = ttk.Frame(main_frame)
        exp_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(exp_frame, text="Ejecutar Pruebas Automáticas", 
                  command=self.run_auto_tests).pack(pady=2)
    
    def init_graph(self):
        """Inicializa la gráfica vacía."""
        self.ax.clear()
        self.ax.set_title("Tiempos de Búsqueda por Tamaño de Lista")
        self.ax.set_xlabel("Tamaño de Lista")
        self.ax.set_ylabel("Tiempo (ms)")
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.canvas.draw()
    
    def generate_data(self):
        """Genera una nueva lista de datos ordenados."""
        try:
            size = int(self.size_combobox.get())
            self.current_size = size
            self.current_list = sorted([random.randint(0, 1000) for _ in range(size)])
            
            # Habilitar botones de búsqueda
            self.linear_btn.config(state=tk.NORMAL)
            self.binary_btn.config(state=tk.NORMAL)
            
            self.show_result(f"Lista generada: {size} elementos ordenados")
        except ValueError:
            messagebox.showerror("Error", "Seleccione un tamaño válido")
    
    def run_search(self, algorithm):
        """Ejecuta el algoritmo de búsqueda especificado."""
        if not self.current_list:
            messagebox.showwarning("Advertencia", "Primero genere una lista")
            return
        
        try:
            target = int(self.search_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido")
            return
        
        # Ejecutar búsqueda
        if algorithm == 'linear':
            index, exec_time = self.linear_search(self.current_list, target)
        else:
            index, exec_time = self.binary_search(self.current_list, target)
        
        # Guardar resultados para la gráfica
        if self.current_size not in self.results[algorithm]['averages']:
            self.results[algorithm]['averages'][self.current_size] = []
        self.results[algorithm]['averages'][self.current_size].append(exec_time)
        
        # Mostrar resultados
        result_str = f"{'Búsqueda Lineal' if algorithm == 'linear' else 'Búsqueda Binaria'} - "
        result_str += f"Tamaño: {self.current_size}\n"
        result_str += f"Valor: {target} - "
        result_str += f"Encontrado en índice {index}" if index is not None else "No encontrado"
        result_str += f"\nTiempo: {exec_time:.6f} ms\n"
        
        self.show_result(result_str)
        self.update_graph()
    
    def linear_search(self, lst, target):
        """Implementación de búsqueda lineal."""
        start_time = time.perf_counter()
        for i in range(len(lst)):
            if lst[i] == target:
                end_time = time.perf_counter()
                return i, (end_time - start_time) * 1000
        end_time = time.perf_counter()
        return None, (end_time - start_time) * 1000
    
    def binary_search(self, lst, target):
        """Implementación de búsqueda binaria iterativa."""
        start_time = time.perf_counter()
        low = 0
        high = len(lst) - 1
        
        while low <= high:
            mid = (high + low) // 2
            if lst[mid] < target:
                low = mid + 1
            elif lst[mid] > target:
                high = mid - 1
            else:
                end_time = time.perf_counter()
                return mid, (end_time - start_time) * 1000
        
        end_time = time.perf_counter()
        return None, (end_time - start_time) * 1000
    
    def run_auto_tests(self):
        """Ejecuta pruebas automáticas para todos los tamaños."""
        sizes = [100, 1000, 10000, 100000]
        repetitions = 5
        
        self.show_result("Iniciando pruebas automáticas...\n")
        
        for size in sizes:
            self.show_result(f"\nTamaño: {size}")
            
            # Generar lista ordenada
            test_list = sorted([random.randint(0, 1000) for _ in range(size)])
            
            # Seleccionar un valor existente para buscar
            target = random.choice(test_list)
            
            # Probar búsqueda lineal
            linear_times = []
            self.show_result(f"  Búsqueda lineal ({repetitions} repeticiones)...")
            for _ in range(repetitions):
                _, time_taken = self.linear_search(test_list, target)
                linear_times.append(time_taken)
            
            # Probar búsqueda binaria
            binary_times = []
            self.show_result(f"  Búsqueda binaria ({repetitions} repeticiones)...")
            for _ in range(repetitions):
                _, time_taken = self.binary_search(test_list, target)
                binary_times.append(time_taken)
            
            # Calcular promedios
            avg_linear = sum(linear_times) / repetitions
            avg_binary = sum(binary_times) / repetitions
            
            # Guardar resultados
            self.results['linear']['averages'][size] = avg_linear
            self.results['binary']['averages'][size] = avg_binary
            
            self.show_result(f"  Promedios - Lineal: {avg_linear:.6f} ms | Binaria: {avg_binary:.6f} ms")
        
        self.show_result("\nPruebas completadas")
        self.update_graph()
    
    def show_result(self, text):
        """Muestra texto en el área de resultados."""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, text + "\n")
        self.result_text.see(tk.END)
        self.result_text.config(state=tk.DISABLED)
    
    def update_graph(self):
        """Actualiza la gráfica con los resultados acumulados."""
        self.ax.clear()
        
        # Obtener tamaños y tiempos
        sizes = sorted({size for algo in self.results.values() for size in algo['averages']})
        
        if not sizes:
            self.ax.set_title("No hay datos para mostrar")
            self.canvas.draw()
            return
        
        # Preparar datos para graficar
        linear_avgs = [self.results['linear']['averages'].get(size, 0) for size in sizes]
        binary_avgs = [self.results['binary']['averages'].get(size, 0) for size in sizes]
        
        # Graficar como líneas (similar a la imagen de referencia)
        line1, = self.ax.plot(sizes, linear_avgs, 'b-', marker='o', label='Búsqueda Lineal')
        line2, = self.ax.plot(sizes, binary_avgs, 'r--', marker='s', label='Búsqueda Binaria')
        
        # Configurar gráfica
        self.ax.set_title("Comparación de Tiempos de Búsqueda", pad=15)
        self.ax.set_xlabel("Tamaño de Lista")
        self.ax.set_ylabel("Tiempo Promedio (ms)")
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.ax.legend()
        
        # Ajustar escala para mejor visualización
        self.ax.set_xscale('log')
        
        # Mostrar valores en los puntos
        for i, size in enumerate(sizes):
            self.ax.text(size, linear_avgs[i], f'{linear_avgs[i]:.2f}', 
                        ha='center', va='bottom', fontsize=8)
            self.ax.text(size, binary_avgs[i], f'{binary_avgs[i]:.2f}', 
                        ha='center', va='top', fontsize=8)
        
        self.canvas.draw()

def main():
    root = tk.Tk()
    app = SearchApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()