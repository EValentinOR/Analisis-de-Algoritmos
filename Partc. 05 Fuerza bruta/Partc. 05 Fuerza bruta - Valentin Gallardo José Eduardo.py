import tkinter as tk
from tkinter import messagebox
import random

#Partc. 05 Fuerza bruta
#Valentin Gallardo José Eduardo


def distancia_paso_a_paso(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    dx = x1 - x2
    dy = y1 - y2
    dx2 = dx * dx
    dy2 = dy * dy
    suma = dx2 + dy2
    distancia = suma ** 0.5
    pasos = (
        f"Comparando puntos {p1} y {p2}:\n"
        f"  dx = {x1} - {x2} = {dx}\n"
        f"  dy = {y1} - {y2} = {dy}\n"
        f"  dx^2 = ({dx})^2 = {dx2}\n"
        f"  dy^2 = ({dy})^2 = {dy2}\n"
        f"  suma = dx^2 + dy^2 = {dx2} + {dy2} = {suma}\n"
        f"  dist = suma^(1/2) = {suma}^(1/2) = {distancia:.6f}\n"
    )
    return distancia, pasos

def par_mas_cercano(puntos):
    min_dist = float('inf')
    mejor_par = None
    pasos_mejor_par = ""
    n = len(puntos)
    for i in range(n):
        for j in range(i + 1, n):
            d, pasos = distancia_paso_a_paso(puntos[i], puntos[j])
            if d < min_dist:
                min_dist = d
                mejor_par = (puntos[i], puntos[j])
                pasos_mejor_par = pasos
    return mejor_par, min_dist, pasos_mejor_par

def calcular():
    try:
        puntos = []
        for i in range(5):
            x = int(entries[i*2].get())
            y = int(entries[i*2+1].get())
            puntos.append((x, y))
        par, dist, pasos = par_mas_cercano(puntos)
        resultado = f"Par más cercano: {par}  |  Distancia: {dist:.6f}"
        messagebox.showinfo("Resultado", resultado)
        text_area.config(state='normal')
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, "Puntos ingresados:\n")
        letras = ["A", "B", "C", "D", "E"]
        for idx, p in enumerate(puntos):
            text_area.insert(tk.END, f"  Punto {letras[idx]}: {p}\n")
        text_area.insert(tk.END, "\n" + resultado + "\n\n")
        text_area.insert(tk.END, "Detalle del cálculo del par más cercano:\n")
        text_area.insert(tk.END, pasos)
        text_area.config(state='disabled')
        print("Puntos:", puntos)
        print(resultado)
        print("Pasos:\n", pasos)
    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa números enteros válidos en todas las entradas.")

def generar_aleatorios():
    for i in range(10):
        valor = random.randint(0, 40)
        entries[i].delete(0, tk.END)
        entries[i].insert(0, str(valor))
    text_area.config(state='normal')
    text_area.delete('1.0', tk.END)
    text_area.config(state='disabled')

ventana = tk.Tk()
ventana.title("Par más cercano - 5 puntos (sin math.sqrt)")
ventana.resizable(False, False)

entries = []
letras = ["A", "B", "C", "D", "E"]
for i in range(5):
    tk.Label(ventana, text=f"Punto {letras[i]} (x, y):").grid(row=i, column=0, padx=6, pady=4, sticky='w')
    ex = tk.Entry(ventana, width=6)
    ey = tk.Entry(ventana, width=6)
    ex.grid(row=i, column=1, padx=4, pady=4)
    ey.grid(row=i, column=2, padx=4, pady=4)
    entries.append(ex)
    entries.append(ey)

btn_calcular = tk.Button(ventana, text="Calcular par más cercano", command=calcular)
btn_calcular.grid(row=6, column=0, columnspan=3, pady=(8,2), sticky='we', padx=6)

btn_aleatorio = tk.Button(ventana, text="Generar aleatorios (0-40)", command=generar_aleatorios)
btn_aleatorio.grid(row=7, column=0, columnspan=3, pady=(0,8), sticky='we', padx=6)

text_area = tk.Text(ventana, width=50, height=10, wrap='word', state='disabled')
text_area.grid(row=8, column=0, columnspan=3, padx=6, pady=(0,10))

ventana.mainloop()
