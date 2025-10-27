import random
import time
import matplotlib.pyplot as plt
from random import sample

# Importamos un Método de la biblioteca random para generar listas aleatorias

lista = list(range(100))  # Creamos la lista base con números del 1 al 100

# Creamos una lista aleatoria con sample
# (8 elementos aleatorios de la lista base)
vectorbs = sample(lista, 8)

def bubblesort(vectorbs):
    """Esta función ordenara el vector que le pases como argumento con el Método de Bubble Sort"""

    # Imprimimos la lista obtenida al principio (Desordenada)
    print("El vector a ordenar es:", vectorbs)
    n = 0  # Establecemos un contador del largo del vector

    for _ in vectorbs:
        n += 1  # Contamos la cantidad de caracteres dentro del vector

    for i in range(n - 1):
        # Le damos un rango n para que complete el proceso.
        for j in range(0, n - i - 1):
            # Revisa la matriz de 0 hasta n-i-1
            if vectorbs[j] > vectorbs[j + 1]:
                vectorbs[j], vectorbs[j + 1] = vectorbs[j + 1], vectorbs[j]
            # Se intercambian si el elemento encontrado es mayor
            # Luego pasa al siguiente
    print("El vector ordenado es: ", vectorbs)

bubblesort(vectorbs)

lista = list(range(100))  # Creamos la lista base con números del 1 al 100

# Creamos una lista aleatoria con sample
# (8 elementos aleatorios de la lista base)
vectorselect = sample(lista, 8)


# Importamos un Método de la biblioteca random para generar listas aleatorias

lista = list(range(100))  # Creamos la lista base con números del 1 al 100

# Creamos una lista aleatoria con sample
# (8 elementos aleatorios de la lista base)
vectormerge = sample(lista, 8)


def mergesort(vectormerge):
    """Esta función ordenara el vector que le pases como argumento
    con el Método Merge Sort"""

    # Imprimimos la lista obtenida al principio (Desordenada)
    print("El vector a ordenar con merge es:", vectormerge)

    def merge(vectormerge):

        def largo(vec):
            largovec = 0  # Establecemos un contador del largovec
            for _ in vec:
                largovec += 1  # Obtenemos el largo del vector
            return largovec

        if largo(vectormerge) > 1:
            medio = largo(vectormerge) // 2  # Buscamos el medio del vector

            # Lo dividimos en 2 partes
            izq = vectormerge[:medio]
            der = vectormerge[medio:]

            merge(izq)  # Mismo procedimiento a la primer mitad
            merge(der)  # Mismo procedimiento a la segunda mitad

            i = j = k = 0

            # Copiamos los datos a los vectores temporales izq[] y der[]
            while i < largo(izq) and j < largo(der):
                if izq[i] < der[j]:
                    vectormerge[k] = izq[i]
                    i += 1
                else:
                    vectormerge[k] = der[j]
                    j += 1
                k += 1

            # Nos fijamos si quedaron elementos en la lista
            # tanto derecha como izquierda
            while i < largo(izq):
                vectormerge[k] = izq[i]
                i += 1
                k += 1

            while j < largo(der):
                vectormerge[k] = der[j]
                j += 1
                k += 1

    merge(vectormerge)
    print("El vector ordenado con merge es: ", vectormerge)


mergesort(vectormerge)

lista = list(range(100)) # Creamos la lista base con números del 1 al 100

# Creamos una lista aleatoria con sample
#(8 elementos aleatorios de la lista base)
vectorquick = sample(lista,8)
def quicksort(vectorquick, start=0, end=len(vectorquick) - 1):
    """Esta función ordenara el vector que le pases como argumento
    con el Método Quick Sort"""

    # Imprimimos la lista obtenida al principio (Desordenada)
    print("El vector a ordenar con quick es:", vectorquick)

    def quick(vectorquick, start=0, end=len(vectorquick) - 1):

        if start >= end:
            return

        def particion(vectorquick, start=0, end=len(vectorquick) - 1):
            pivot = vectorquick[start]
            menor = start + 1
            mayor = end

            while True:
                # Si el valor actual es mayor que el pivot
                # está en el lugar correcto (lado derecho del pivot) y podemos
                # movernos hacia la izquierda, al siguiente elemento.
                # También debemos asegurarnos de no haber superado el puntero bajo, ya que indica
                # que ya hemos movido todos los elementos a su lado correcto del pivot
                while menor <= mayor and vectorquick[mayor] >= pivot:
                    mayor = mayor - 1

                # Proceso opuesto al anterior
                while menor <= mayor and vectorquick[menor] <= pivot:
                    menor = menor + 1

                # Encontramos un valor sea mayor o menor y que este fuera del arreglo
                # ó menor es más grande que mayor, en cuyo caso salimos del ciclo
                if menor <= mayor:
                    vectorquick[menor], vectorquick[mayor] = vectorquick[mayor], vectorquick[menor]
                    # Continua el bucle
                else:
                    # Salimos del bucle
                    break

            vectorquick[start], vectorquick[mayor] = vectorquick[mayor], vectorquick[start]

            return mayor

        p = particion(vectorquick, start, end)
        quick(vectorquick, start, p - 1)
        quick(vectorquick, p + 1, end)

    quick(vectorquick)
    print("El vector ordenado con quick es:", vectorquick)


quicksort(vectorquick)



# Llamar a la función para generar la gráfica
def generar_grafica_comparativa():
    # Lista de tamaños de entrada para probar (empezando con tamaños más pequeños)
    tamanios = [10, 50, 100, 200, 500, 1000]

    # Almacenar tiempos de ejecución para cada algoritmo
    tiempos_bubble = []
    tiempos_merge = []
    tiempos_quick = []

    for tamanio in tamanios:
        # Generar lista aleatoria del tamaño actual
        lista_base = list(range(tamanio))
        vector = sample(lista_base, tamanio)

        print(f"Probando con tamaño: {tamanio}")

        # Bubble Sort (solo para tamaños pequeños)
        if tamanio <= 500:  # Limitar bubble sort a tamaños manejables
            vector_copy = vector.copy()
            inicio = time.time()
            n = len(vector_copy)
            for i in range(n - 1):
                for j in range(0, n - i - 1):
                    if vector_copy[j] > vector_copy[j + 1]:
                        vector_copy[j], vector_copy[j + 1] = vector_copy[j + 1], vector_copy[j]
            fin = time.time()
            tiempos_bubble.append(fin - inicio)
        else:
            tiempos_bubble.append(None)  # Para mantener la alineación de datos

        # Merge Sort
        vector_copy = vector.copy()
        inicio = time.time()

        def merge_sort(arr):
            if len(arr) > 1:
                medio = len(arr) // 2
                izq = arr[:medio]
                der = arr[medio:]

                merge_sort(izq)
                merge_sort(der)

                i = j = k = 0

                while i < len(izq) and j < len(der):
                    if izq[i] < der[j]:
                        arr[k] = izq[i]
                        i += 1
                    else:
                        arr[k] = der[j]
                        j += 1
                    k += 1

                while i < len(izq):
                    arr[k] = izq[i]
                    i += 1
                    k += 1

                while j < len(der):
                    arr[k] = der[j]
                    j += 1
                    k += 1

        merge_sort(vector_copy)
        fin = time.time()
        tiempos_merge.append(fin - inicio)

        # Quick Sort (con manejo de recursión mejorado)
        vector_copy = vector.copy()
        inicio = time.time()

        def quick_sort(arr, start=0, end=None):
            if end is None:
                end = len(arr) - 1

            if start >= end:
                return

            # Elegir pivote como elemento medio para mejor rendimiento
            medio = (start + end) // 2
            arr[start], arr[medio] = arr[medio], arr[start]

            pivot = arr[start]
            izquierda = start + 1
            derecha = end

            while izquierda <= derecha:
                while izquierda <= derecha and arr[izquierda] <= pivot:
                    izquierda += 1
                while izquierda <= derecha and arr[derecha] >= pivot:
                    derecha -= 1
                if izquierda < derecha:
                    arr[izquierda], arr[derecha] = arr[derecha], arr[izquierda]

            arr[start], arr[derecha] = arr[derecha], arr[start]

            # Ordenar recursivamente las dos mitades
            quick_sort(arr, start, derecha - 1)
            quick_sort(arr, derecha + 1, end)

        try:
            quick_sort(vector_copy)
            fin = time.time()
            tiempos_quick.append(fin - inicio)
        except RecursionError:
            print(f"RecursionError con Quick Sort en tamaño {tamanio}")
            tiempos_quick.append(None)

    # Filtrar valores None para la gráfica
    tamanios_filtrados = []
    bubble_filtrado = []
    merge_filtrado = []
    quick_filtrado = []

    for i in range(len(tamanios)):
        if tiempos_bubble[i] is not None and tiempos_quick[i] is not None:
            tamanios_filtrados.append(tamanios[i])
            bubble_filtrado.append(tiempos_bubble[i])
            merge_filtrado.append(tiempos_merge[i])
            quick_filtrado.append(tiempos_quick[i])

    # Crear la gráfica comparativa con escala normal
    plt.figure(figsize=(12, 6))

    plt.plot(tamanios_filtrados, bubble_filtrado, marker='o', label='Bubble Sort', linewidth=2)
    plt.plot(tamanios_filtrados, merge_filtrado, marker='s', label='Merge Sort', linewidth=2)
    plt.plot(tamanios_filtrados, quick_filtrado, marker='^', label='Quick Sort', linewidth=2)

    plt.xlabel('Tamaño de la Lista')
    plt.ylabel('Tiempo de Ejecución (segundos)')
    plt.title('Comparación de Tiempos de Ejecución de Algoritmos de Ordenamiento')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Solo usar escala logarítmica en el eje Y si es necesario
    max_tiempo = max(max(bubble_filtrado), max(merge_filtrado), max(quick_filtrado))
    if max_tiempo / min([t for t in bubble_filtrado + merge_filtrado + quick_filtrado if t > 0]) > 100:
        plt.yscale('log')
        plt.ylabel('Tiempo de Ejecución (segundos) - Escala Logarítmica')

    plt.tight_layout()
    plt.show()

    # Imprimir resultados en tabla
    print("\nResultados de tiempos de ejecución (segundos):")
    print("Tamaño\tBubble Sort\tMerge Sort\tQuick Sort")
    print("-" * 50)
    for i in range(len(tamanios_filtrados)):
        print(f"{tamanios_filtrados[i]}\t{bubble_filtrado[i]:.6f}\t{merge_filtrado[i]:.6f}\t{quick_filtrado[i]:.6f}")


# Llamar a la función para generar la gráfica
generar_grafica_comparativa()