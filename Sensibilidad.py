import numpy as np
from scipy.optimize import linprog
import tkinter as tk
from tkinter import ttk, messagebox

def analizar_sensibilidad(c, A, B, delta_B):
    resultados = []
    for delta in delta_B:
        B_modificado = B + delta
        res = linprog(c, A_eq=A, b_eq=B_modificado, method='highs')
        if res.success:
            resultados.append({
                "B_modificado": B_modificado,
                "solucion": res.x,
                "valor_objetivo": res.fun
            })
        else:
            resultados.append({
                "B_modificado": B_modificado,
                "solucion": None,
                "valor_objetivo": None
            })
    return resultados

def ejecutar_analisis():
    try:
        # Leer la cantidad de variables y restricciones
        n_variables = int(variables_entry.get())
        n_restricciones = int(restricciones_entry.get())
        
        # Leer los coeficientes de c
        c = list(map(float, c_entry.get().split(',')))
        if len(c) != n_variables:
            raise ValueError("Los coeficientes de c no coinciden con la cantidad de variables.")
        
        # Leer la matriz A
        A = []
        for i in range(n_restricciones):
            fila = list(map(float, matriz_entries[i].get().split(',')))
            if len(fila) != n_variables:
                raise ValueError(f"Fila {i+1} de la matriz A tiene un número incorrecto de coeficientes.")
            A.append(fila)
        A = np.array(A)
        
        # Leer el vector B
        B = list(map(float, b_entry.get().split(',')))
        if len(B) != n_restricciones:
            raise ValueError("El vector B no coincide con la cantidad de restricciones.")
        B = np.array(B)
        
        # Leer los cambios en B
        delta_B = []
        for delta in delta_entries:
            cambio = list(map(float, delta.get().split(',')))
            if len(cambio) != n_restricciones:
                raise ValueError("Un cambio en B no coincide con la cantidad de restricciones.")
            delta_B.append(np.array(cambio))
        
        # Realizar el análisis de sensibilidad
        resultados = analizar_sensibilidad(c, A, B, delta_B)
        
        # Mostrar resultados
        resultados_text.delete(1.0, tk.END)
        for i, resultado in enumerate(resultados):
            resultados_text.insert(tk.END, f"Cambio {i+1}:\n")
            resultados_text.insert(tk.END, f"B modificado: {resultado['B_modificado']}\n")
            if resultado["solucion"] is not None:
                resultados_text.insert(tk.END, f"Solución óptima: {resultado['solucion']}\n")
                resultados_text.insert(tk.END, f"Valor objetivo: {resultado['valor_objetivo']}\n")
            else:
                resultados_text.insert(tk.END, "No se pudo encontrar una solución factible.\n")
            resultados_text.insert(tk.END, "-"*40 + "\n")
    
    except ValueError as e:
        messagebox.showerror("Error de entrada", str(e))

# Crear ventana principal
root = tk.Tk()
root.title("Análisis de Sensibilidad")

# Entrada para cantidad de variables y restricciones
frame_top = ttk.Frame(root)
frame_top.pack(pady=10)

ttk.Label(frame_top, text="Cantidad de variables:").grid(row=0, column=0, padx=5)
variables_entry = ttk.Entry(frame_top)
variables_entry.grid(row=0, column=1, padx=5)

ttk.Label(frame_top, text="Cantidad de restricciones:").grid(row=1, column=0, padx=5)
restricciones_entry = ttk.Entry(frame_top)
restricciones_entry.grid(row=1, column=1, padx=5)

# Entrada para los coeficientes de c
ttk.Label(root, text="Coeficientes de c (separados por comas):").pack(pady=5)
c_entry = ttk.Entry(root, width=50)
c_entry.pack()

# Entrada para la matriz A
ttk.Label(root, text="Matriz A (una fila por línea, coeficientes separados por comas):").pack(pady=5)
matriz_frame = ttk.Frame(root)
matriz_frame.pack()

matriz_entries = []

def actualizar_matriz():
    for widget in matriz_frame.winfo_children():
        widget.destroy()
    try:
        n_restricciones = int(restricciones_entry.get())
        matriz_entries.clear()
        for i in range(n_restricciones):
            entry = ttk.Entry(matriz_frame, width=50)
            entry.pack(pady=2)
            matriz_entries.append(entry)
    except ValueError:
        messagebox.showerror("Error", "Ingrese un número válido de restricciones.")

restricciones_entry.bind("<FocusOut>", lambda e: actualizar_matriz())

# Entrada para el vector B
ttk.Label(root, text="Vector B (separados por comas):").pack(pady=5)
b_entry = ttk.Entry(root, width=50)
b_entry.pack()

# Entrada para los cambios en B
ttk.Label(root, text="Cambios en B (una fila por línea, separados por comas):").pack(pady=5)
delta_frame = ttk.Frame(root)
delta_frame.pack()

delta_entries = []

def agregar_cambio():
    entry = ttk.Entry(delta_frame, width=50)
    entry.pack(pady=2)
    delta_entries.append(entry)

ttk.Button(root, text="Agregar cambio en B", command=agregar_cambio).pack(pady=5)

# Botón para ejecutar análisis
ttk.Button(root, text="Ejecutar Análisis", command=ejecutar_analisis).pack(pady=10)

# Resultados
ttk.Label(root, text="Resultados:").pack(pady=5)
resultados_text = tk.Text(root, width=80, height=20)
resultados_text.pack()

# Iniciar aplicación
root.mainloop()
