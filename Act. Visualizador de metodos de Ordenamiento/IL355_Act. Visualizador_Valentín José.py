import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Act. Visualizador de metodos de Ordenamiento
# Cuellar Hernandez Cinthya Sofia
# Valentin Gallardo Jose Eduardo
# Analisis de Algoritmos - seccion D01

class SortApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Comparador de Algoritmos de Ordenamiento")
        self.root.geometry("1000x800")

        # Parámetros para la visualización de algoritmos de ordenamiento
        self.ANCHO = 800
        self.ALTO = 300
        self.N_BARRAS = 40
        self.VAL_MIN, self.VAL_MAX = 5, 100
        self.RETARDO_MS = 50  # velocidad en milisegundos
        self.datos = []
        self.sort_gen = None
        self.sorting = False  # Para controlar si está ordenando
        self.mostrar_resaltados = True  # Controlar si se muestran los resaltados
        
        # Resultados de tiempos de ordenamiento (almacena tamaño y tiempo)
        self.tiempos_ordenamiento = {
            'Selection Sort': {},
            'Bubble Sort': {},
            'Merge Sort': {},
            'Quick Sort': {}
        }
        self.ultimo_tiempo = None  # Para almacenar el último tiempo medido

        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure('TFrame', padding=5)
        self.style.configure('TButton', padding=5)
        self.style.configure('TLabel', padding=5)

        # Crear frame principal
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Inicializar interfaz
        self.create_sort_widgets()
        self.init_graph()

    def create_sort_widgets(self):
        """Crea todos los widgets de la interfaz de ordenamiento."""
        # Frame de ordenamiento
        sort_frame = ttk.LabelFrame(self.main_frame, text="Algoritmos de Ordenamiento")
        sort_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Canvas para dibujar las barras
        self.sort_canvas = tk.Canvas(sort_frame, width=self.ANCHO, height=self.ALTO, bg="white")
        self.sort_canvas.pack(padx=10, pady=10)

        # Panel de botones
        panel = ttk.Frame(sort_frame)
        panel.pack(pady=6)

        ttk.Button(panel, text="Generar", command=self.generar_datos).pack(side="left", padx=5)
        ttk.Button(panel, text="Ordenar", command=self.iniciar_ordenamiento).pack(side="left", padx=5)
        ttk.Button(panel, text="Mezclar", command=self.mezclar_datos).pack(side="left", padx=5)
        ttk.Button(panel, text="Limpiar", command=self.limpiar_visualizacion).pack(side="left", padx=5)
        ttk.Button(panel, text="Actualizar Gráfica", command=self.actualizar_grafica).pack(side="left", padx=5)

        # Controles de algoritmo y parámetros
        control_frame = ttk.Frame(sort_frame)
        control_frame.pack(pady=5)

        # Dropdown para seleccionar algoritmo
        ttk.Label(control_frame, text="Algoritmo:").pack(side="left")
        self.algoritmo_var = tk.StringVar()
        algoritmos = ["Selection Sort", "Bubble Sort", "Merge Sort", "Quick Sort"]
        self.algoritmo_combo = ttk.Combobox(control_frame, textvariable=self.algoritmo_var, 
                                           values=algoritmos, state="readonly", width=15)
        self.algoritmo_combo.current(0)
        self.algoritmo_combo.pack(side="left", padx=5)

        # Control de tamaño
        ttk.Label(control_frame, text="N:").pack(side="left", padx=(20, 5))
        self.size_var = tk.StringVar(value=str(self.N_BARRAS))
        size_entry = ttk.Entry(control_frame, textvariable=self.size_var, width=5)
        size_entry.pack(side="left")
        ttk.Button(control_frame, text="Aplicar", command=self.actualizar_tamano).pack(side="left", padx=5)

        # Control de velocidad
        ttk.Label(control_frame, text="Velocidad:").pack(side="left", padx=(20, 5))
        self.speed_scale = ttk.Scale(control_frame, from_=0, to=200, 
                                     command=self.actualizar_velocidad, length=150)
        self.speed_scale.set(self.RETARDO_MS)
        self.speed_scale.pack(side="left", padx=5)

        # Estado inicial
        self.generar_datos()

        # Frame de gráfica de comparación
        graph_frame = ttk.LabelFrame(self.main_frame, text="Comparación de Tiempos de Ordenamiento (ms)")
        graph_frame.pack(fill=tk.BOTH, expand=True)

        # Configurar figura de matplotlib
        self.fig, self.ax = plt.subplots(figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def init_graph(self):
        """Inicializa la gráfica vacía."""
        self.ax.clear()
        self.ax.set_title("Tiempos de Ordenamiento por Tamaño de Lista")
        self.ax.set_xlabel("Tamaño de Lista")
        self.ax.set_ylabel("Tiempo (ms)")
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.canvas.draw()

    # ---------------------------
    # Funciones para algoritmos de ordenamiento
    # ---------------------------
    def selection_sort_steps(self, data, draw_callback):
        """Selection Sort paso a paso."""
        inicio = time.perf_counter()
        n = len(data)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if self.mostrar_resaltados:
                    draw_callback(activos=[i, j, min_idx])
                else:
                    draw_callback(activos=[])
                yield
                if data[j] < data[min_idx]:
                    min_idx = j
            # Intercambio
            data[i], data[min_idx] = data[min_idx], data[i]
            if self.mostrar_resaltados:
                draw_callback(activos=[i, min_idx])
            else:
                draw_callback(activos=[])
            yield
        fin = time.perf_counter()
        self.ultimo_tiempo = (fin - inicio) * 1000
        draw_callback(activos=[])

    def bubble_sort_steps(self, data, draw_callback):
        """Bubble Sort paso a paso."""
        inicio = time.perf_counter()
        n = len(data)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if self.mostrar_resaltados:
                    draw_callback(activos=[j, j + 1])
                else:
                    draw_callback(activos=[])
                yield
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
                    swapped = True
                    if self.mostrar_resaltados:
                        draw_callback(activos=[j, j + 1])
                    else:
                        draw_callback(activos=[])
                    yield
            if not swapped:
                break
        fin = time.perf_counter()
        self.ultimo_tiempo = (fin - inicio) * 1000
        draw_callback(activos=[])

    def merge_sort_steps(self, data, draw_callback, start=0, end=None, temp=None):
        """Merge Sort paso a paso."""
        inicio = time.perf_counter()
        if end is None:
            end = len(data) - 1
        if temp is None:
            temp = data[:]
            
        if start < end:
            mid = (start + end) // 2
            
            # Ordenar la primera mitad
            yield from self.merge_sort_steps(data, draw_callback, start, mid, temp)
            
            # Ordenar la segunda mitad
            yield from self.merge_sort_steps(data, draw_callback, mid + 1, end, temp)
            
            # Combinar las mitades ordenadas
            yield from self.merge_steps(data, draw_callback, start, mid, end, temp)
        fin = time.perf_counter()
        self.ultimo_tiempo = (fin - inicio) * 1000

    def merge_steps(self, data, draw_callback, start, mid, end, temp):
        """Función de mezcla para Merge Sort."""
        i, j, k = start, mid + 1, start
        
        while i <= mid and j <= end:
            if self.mostrar_resaltados:
                draw_callback(activos=[i, j])
            else:
                draw_callback(activos=[])
            yield
            if data[i] <= data[j]:
                temp[k] = data[i]
                i += 1
            else:
                temp[k] = data[j]
                j += 1
            k += 1
            
        while i <= mid:
            temp[k] = data[i]
            i += 1
            k += 1
            
        while j <= end:
            temp[k] = data[j]
            j += 1
            k += 1
            
        for idx in range(start, end + 1):
            data[idx] = temp[idx]
            if self.mostrar_resaltados:
                draw_callback(activos=[idx])
            else:
                draw_callback(activos=[])
            yield

    def quick_sort_steps(self, data, draw_callback, low=0, high=None):
        """Quick Sort paso a paso."""
        inicio = time.perf_counter()
        if high is None:
            high = len(data) - 1

        if low < high:
            # Particionar y obtener la posición del pivote
            pivot_idx = yield from self.partition_steps(data, low, high, draw_callback)

            # Recursivamente ordenar los elementos antes y después de la partición
            yield from self.quick_sort_steps(data, draw_callback, low, pivot_idx - 1)
            yield from self.quick_sort_steps(data, draw_callback, pivot_idx + 1, high)
        fin = time.perf_counter()
        self.ultimo_tiempo = (fin - inicio) * 1000

    def partition_steps(self, data, low, high, draw_callback):
        """Función de partición para Quick Sort."""
        pivot = data[high]
        i = low - 1

        for j in range(low, high):
            if self.mostrar_resaltados:
                draw_callback(activos=[j, high, i])
            else:
                draw_callback(activos=[])
            yield
            if data[j] <= pivot:
                i += 1
                data[i], data[j] = data[j], data[i]
                if self.mostrar_resaltados:
                    draw_callback(activos=[i, j, high])
                else:
                    draw_callback(activos=[])
                yield

        data[i + 1], data[high] = data[high], data[i + 1]
        if self.mostrar_resaltados:
            draw_callback(activos=[i + 1, high])
        else:
            draw_callback(activos=[])
        yield
        return i + 1

    def dibujar_barras(self, datos, activos=None):
        """Dibuja las barras en el canvas."""
        self.sort_canvas.delete("all")
        if not datos:
            return
        n = len(datos)
        margen = 10
        ancho_disp = self.ANCHO - 2 * margen
        alto_disp = self.ALTO - 2 * margen
        w = ancho_disp / n
        esc = alto_disp / max(datos)

        for i, v in enumerate(datos):
            x0 = margen + i * w
            x1 = x0 + w * 0.9
            h = v * esc
            y0 = self.ALTO - margen - h
            y1 = self.ALTO - margen

            color = "#4e79a7"  # azul normal
            # Solo mostrar naranja si hay resaltados activos y la opción está habilitada
            if activos and i in activos and self.mostrar_resaltados:
                color = "#f28e2b"  # naranja para comparaciones/intercambios
            self.sort_canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

        self.sort_canvas.create_text(6, 6, anchor="nw", text=f"n={len(datos)}", fill="#666")

    def generar_datos(self):
        """Genera lista de números aleatorios y dibuja."""
        if self.sorting:
            messagebox.showwarning("Advertencia", "Espere a que termine el ordenamiento actual")
            return
            
        random.seed(time.time())
        self.datos = [random.randint(self.VAL_MIN, self.VAL_MAX) for _ in range(self.N_BARRAS)]
        self.dibujar_barras(self.datos)
        self.sort_gen = None  # Reiniciar el generador
        self.mostrar_resaltados = True  # Restablecer la visualización de resaltados

    def mezclar_datos(self):
        """Mezcla los datos actuales."""
        if self.sorting:
            messagebox.showwarning("Advertencia", "Espere a que termine el ordenamiento actual")
            return
            
        random.shuffle(self.datos)
        self.dibujar_barras(self.datos)
        self.sort_gen = None  # Reiniciar el generador
        self.mostrar_resaltados = True  # Restablecer la visualización de resaltados

    def limpiar_visualizacion(self):
        """Limpia la visualización (desactiva resaltados durante el ordenamiento)."""
        if self.sorting:
            # Si está ordenando, desactiva los resaltados para el resto del proceso
            self.mostrar_resaltados = False
            # Redibuja inmediatamente sin resaltados
            self.dibujar_barras(self.datos, activos=[])
        else:
            # If no está ordenando, redibuja normalmente
            self.dibujar_barras(self.datos)
            self.mostrar_resaltados = True

    def iniciar_ordenamiento(self):
        """Inicia el ordenamiento según el algoritmo seleccionado."""
        if self.sorting:
            messagebox.showwarning("Advertencia", "Ya hay un ordenamiento en curso")
            return
            
        if not self.datos:
            return
            
        algoritmo = self.algoritmo_var.get()
        
        # Asegurarse de que los resaltados estén activados al iniciar
        self.mostrar_resaltados = True
        
        # Si no hay un generador activo, crear uno nuevo según el algoritmo seleccionado
        if self.sort_gen is None:
            if algoritmo == "Selection Sort":
                self.sort_gen = self.selection_sort_steps(self.datos,
                                                          lambda activos=None: self.dibujar_barras(self.datos, activos))
            elif algoritmo == "Bubble Sort":
                self.sort_gen = self.bubble_sort_steps(self.datos,
                                                       lambda activos=None: self.dibujar_barras(self.datos, activos))
            elif algoritmo == "Merge Sort":
                self.sort_gen = self.merge_sort_steps(self.datos,
                                                      lambda activos=None: self.dibujar_barras(self.datos, activos))
            elif algoritmo == "Quick Sort":
                self.sort_gen = self.quick_sort_steps(self.datos,
                                                      lambda activos=None: self.dibujar_barras(self.datos, activos))
            else:
                messagebox.showerror("Error", "Seleccione un algoritmo válido")
                return

        self.sorting = True
        self.ultimo_tiempo = None
        self.ejecutar_paso()

    def ejecutar_paso(self):
        """Ejecuta un paso del algoritmo de ordenamiento."""
        try:
            next(self.sort_gen)  # avanza un paso del algoritmo
            self.root.after(self.RETARDO_MS, self.ejecutar_paso)  # agenda el siguiente paso
        except StopIteration:
            self.sort_gen = None  # terminó, permitir reinicio
            self.sorting = False
            # Al terminar, asegurarse de que no hay elementos resaltados
            self.dibujar_barras(self.datos, activos=[])
            self.mostrar_resaltados = True  # Restablecer para la próxima vez
            
            # Mostrar el tiempo que tomó el ordenamiento
            if self.ultimo_tiempo is not None:
                algoritmo = self.algoritmo_var.get()
                messagebox.showinfo("Ordenamiento Completado", 
                                  f"{algoritmo} completado en {self.ultimo_tiempo:.2f} ms")

    def actualizar_velocidad(self, valor):
        """Actualiza la velocidad de la animación."""
        self.RETARDO_MS = int(float(valor))

    def actualizar_tamano(self):
        """Actualiza el tamaño del array y regenera los datos."""
        if self.sorting:
            messagebox.showwarning("Advertencia", "Espere a que termine el ordenamiento actual")
            return
            
        try:
            nuevo_tamano = int(self.size_var.get())
            if 10 <= nuevo_tamano <= 100:
                self.N_BARRAS = nuevo_tamano
                self.generar_datos()
            else:
                messagebox.showerror("Error", "El tamaño debe estar entre 10 y 100")
                self.size_var.set(str(self.N_BARRAS))
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido")
            self.size_var.set(str(self.N_BARRAS))

    def actualizar_grafica(self):
        """Actualiza la gráfica con los tiempos de ordenamiento registrados."""
        if self.ultimo_tiempo is None:
            messagebox.showinfo("Información", "Primero ejecute un algoritmo de ordenamiento para registrar tiempos.")
            return
            
        algoritmo = self.algoritmo_var.get()
        tamaño = self.N_BARRAS
        
        # Registrar el tiempo para este algoritmo y tamaño
        if tamaño not in self.tiempos_ordenamiento[algoritmo]:
            self.tiempos_ordenamiento[algoritmo][tamaño] = []
        
        self.tiempos_ordenamiento[algoritmo][tamaño].append(self.ultimo_tiempo)
        
        # Actualizar la gráfica
        self.update_graph()
        
        messagebox.showinfo("Gráfica Actualizada", 
                          f"Tiempo de {algoritmo} para n={tamaño}: {self.ultimo_tiempo:.2f} ms\nLa gráfica ha sido actualizada.")

    def update_graph(self):
        """Actualiza la gráfica con los resultados de tiempos de ordenamiento."""
        self.ax.clear()

        # Obtener todos los tamaños únicos que han sido probados
        todos_tamanios = set()
        for algoritmo in self.tiempos_ordenamiento.values():
            todos_tamanios.update(algoritmo.keys())
        
        if not todos_tamanios:
            self.ax.set_title("Ejecute algoritmos de ordenamiento y luego 'Actualizar Gráfica'")
            self.ax.set_xlabel("Tamaño de Lista")
            self.ax.set_ylabel("Tiempo (ms)")
            self.ax.grid(True, linestyle='--', alpha=0.6)
            self.canvas.draw()
            return

        # Ordenar los tamaños
        tamanios_ordenados = sorted(todos_tamanios)
        
        # Colores para cada algoritmo
        colores = ['blue', 'red', 'green', 'orange']
        algoritmos = list(self.tiempos_ordenamiento.keys())
        
        # Graficar cada algoritmo
        for i, algoritmo in enumerate(algoritmos):
            tiempos_promedio = []
            for tamaño in tamanios_ordenados:
                if tamaño in self.tiempos_ordenamiento[algoritmo] and self.tiempos_ordenamiento[algoritmo][tamaño]:
                    # Calcular promedio de tiempos para este tamaño
                    promedio = sum(self.tiempos_ordenamiento[algoritmo][tamaño]) / len(self.tiempos_ordenamiento[algoritmo][tamaño])
                    tiempos_promedio.append(promedio)
                else:
                    tiempos_promedio.append(0)  # o None si prefieres saltar este punto
            
            # Solo graficar si hay datos
            if any(tiempos_promedio):
                line, = self.ax.plot(tamanios_ordenados, tiempos_promedio, 
                                    marker='o', linestyle='-', color=colores[i], label=algoritmo)
                
                # Añadir etiquetas de valores
                for j, tiempo in enumerate(tiempos_promedio):
                    if tiempo > 0:
                        self.ax.text(tamanios_ordenados[j], tiempo, f'{tiempo:.1f}', 
                                    ha='center', va='bottom', fontsize=8)

        # Configurar gráfica
        self.ax.set_title("Comparación de Tiempos de Ordenamiento", pad=15)
        self.ax.set_xlabel("Tamaño de Lista (n)")
        self.ax.set_ylabel("Tiempo Promedio (ms)")
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.ax.legend()
        
        # Usar escala logarítmica si los valores son muy diferentes
        max_tiempo = max([max(tiempos) for algo in self.tiempos_ordenamiento.values() 
                         for tiempos in algo.values() if tiempos], default=0)
        if max_tiempo > 1000:
            self.ax.set_yscale('log')

        self.canvas.draw()


def main():
    root = tk.Tk()
    app = SortApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()