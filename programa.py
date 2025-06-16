import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import re

# Función para reemplazar las funciones matemáticas por las de numpy
def convertir_a_np(funcion):
    # Reemplazar sin() por np.sin()
    funcion = re.sub(r'\bsin\(', 'np.sin(', funcion)
    # Reemplazar cos() por np.cos()
    funcion = re.sub(r'\bcos\(', 'np.cos(', funcion)
    # Reemplazar tan() por np.tan()
    funcion = re.sub(r'\btan\(', 'np.tan(', funcion)
    # Reemplazar exp() por np.exp()
    funcion = re.sub(r'\bexp\(', 'np.exp(', funcion)
    # Reemplazar log() por np.log()
    funcion = re.sub(r'\blog\(', 'np.log(', funcion)
    # Reemplazar sqrt() por np.sqrt()
    funcion = re.sub(r'\bsqrt\(', 'np.sqrt(', funcion)
    # Reemplazar abs() por np.abs()
    funcion = re.sub(r'\babs\(', 'np.abs(', funcion)
    # Agregar más funciones de numpy según sea necesario...
    return funcion

# Función para manejar la entrada desde el teclado en la calculadora
def on_key(event):
    key = event.char
    if key.isdigit() or key in "+-*/.":
        btn_click(key)
    elif key == '\r':
        btn_equal(repeat=True)
    elif key == '\x08':  # Backspace
        global expression
        expression = expression[:-1]
        input_text.set(expression)

# Función para manejar los clics en los botones de la calculadora
def btn_click(item):
    global expression, last_operation
    if input_text.get() == result and str(item) not in "+-*/":
        expression = str(item)
    else:
        expression += str(item)
    input_text.set(expression)
    last_operation = ""

# Función para evaluar la expresión matemática ingresada en la calculadora
def btn_equal(repeat=False):
    global expression, result, last_operation
    try:
        if repeat and last_operation:
            expression = result + last_operation
        result = str(eval(expression))
        history.set(expression + " = " + result)
        input_text.set(result)
        last_operation = expression[len(result):]
        expression = result
    except Exception as e:
        input_text.set("Error")
        expression = ""
        last_operation = ""

# Función para limpiar el campo de entrada de la calculadora
def btn_clear():
    global expression, last_operation
    expression = ""
    last_operation = ""
    input_text.set("")
    history.set("")

# Función para cambiar de modo (calculadora, promedios, gráficos)
def change_mode(mode):
    calc_frame.pack_forget()
    weighted_avg_frame.pack_forget()
    graph_frame.pack_forget()
    
    if mode == "calculadora":
        calc_frame.pack(expand=True, fill='both')
    elif mode == "promedios":
        weighted_avg_frame.pack(expand=True, fill='both')
        actualizar_campos()
    elif mode == "graficos":
        graph_frame.pack(expand=True, fill='both')

# Función para calcular el promedio ponderado
def calcular_promedio():
    try:
        total = 0
        peso_total = 0
        for i in range(num_notas.get()):
            nota = float(notas[i].get())
            peso = float(pesos[i].get())
            total += nota * peso
            peso_total += peso
        promedio = total / peso_total if peso_total != 0 else 0
        promedio_label.config(text=f"Promedio Ponderado: {promedio:.2f}")
    except ValueError:
        promedio_label.config(text="Error en la entrada de datos")

# Función para actualizar los campos de notas y pesos según el número seleccionado
def actualizar_campos(new_num_notas=None):
    global notas_frame
    
    # Si se proporciona new_num_notas, actualizamos num_notas
    if new_num_notas is not None:
        num_notas.set(new_num_notas)
    
    # Eliminar todos los widgets dentro de notas_frame antes de actualizarlos
    for widget in notas_frame.winfo_children():
        widget.destroy()
    
    # Crear nuevos widgets según el número de notas seleccionado
    for i in range(num_notas.get()):
        ttk.Label(notas_frame, text=f"Nota {i+1}", font=('Arial', 12)).grid(row=i, column=0, padx=5, pady=5)
        tk.Entry(notas_frame, textvariable=notas[i], font=('Arial', 12), width=6).grid(row=i, column=1, padx=5, pady=5)
        ttk.Label(notas_frame, text=f"Peso {i+1}", font=('Arial', 12)).grid(row=i, column=2, padx=5, pady=5)
        tk.Entry(notas_frame, textvariable=pesos[i], font=('Arial', 12), width=6).grid(row=i, column=3, padx=5, pady=5)

# Función para graficar una función matemática ingresada por el usuario
def graficar_funcion(event=None):
    funcion = funcion_entry.get().strip()

    # Convertir la expresión a formato numpy
    funcion = convertir_a_np(funcion)
    
    try:
        # Limpiar el mensaje de resultado
        graph_result_label.config(text="")
        
        # Crear un rango de valores x
        x = np.linspace(-10, 10, 400)
        
        # Evaluar la función ingresada por el usuario
        y = eval(funcion)
        
        # Graficar la función
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set(title=f"Gráfico de {funcion}", xlabel="x", ylabel="y")
        ax.grid(True)
        
        # Limpiar el marco existente y mostrar el nuevo gráfico
        for widget in graph_plot_frame.winfo_children():
            widget.destroy()
        
        canvas = FigureCanvasTkAgg(fig, master=graph_plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both')
    
    except Exception as e:
        # Mostrar un mensaje de error en la etiqueta de resultado
        graph_result_label.config(text=f"Error: {str(e)}")

# Función para mostrar la ventana de ayuda
def mostrar_ayuda():
    ayuda_texto = """
    Ayuda para el Graficador de Funciones
    
    Para graficar una función:
    - Ingresa la función matemática en el campo de texto.
    - Presiona Enter o haz clic en el botón 'Graficar'.
    
    Ejemplos de funciones admitidas:
    - Funciones trigonométricas: sin(x), cos(x), tan(x)
    - Operaciones matemáticas: +, -, *, /
    
    Ten en cuenta:
    - Utiliza 'x' como variable independiente en las funciones.
    """
    
    messagebox.showinfo("Ayuda - Graficador de Funciones", ayuda_texto)

# Configuración principal de tkinter
root = tk.Tk()
root.title("Best Calc Ever")
root.geometry("600x600")
root.resizable(True, True)

expression = ""
result = ""
last_operation = ""
input_text = tk.StringVar()
history = tk.StringVar()

# Agregar un botón de ayuda en la interfaz principal
ayuda_button = ttk.Button(root, text="Ayuda Graficadora", command=mostrar_ayuda)
ayuda_button.pack(pady=10)

# Configuración de los marcos principales
calc_frame = tk.Frame(root)
weighted_avg_frame = tk.Frame(root)
graph_frame = tk.Frame(root)

# Configuración del modo de selección
mode_frame = tk.Frame(root)
mode_frame.pack()

ttk.Button(mode_frame, text="Calculadora", command=lambda: change_mode("calculadora")).pack(side=tk.LEFT)
ttk.Button(mode_frame, text="Promedios", command=lambda: change_mode("promedios")).pack(side=tk.LEFT)
ttk.Button(mode_frame, text="Gráficos", command=lambda: change_mode("graficos")).pack(side=tk.LEFT)

# Configuración del marco de entrada de la calculadora
input_frame = tk.Frame(calc_frame)
input_frame.pack()

input_field = tk.Entry(input_frame, textvariable=input_text, font=('Arial', 18, 'bold'), bd=5, insertwidth=4, justify='right', state='readonly')
input_field.pack(ipady=10, fill='x')

history_field = tk.Entry(input_frame, textvariable=history, font=('Arial', 12), bd=5, insertwidth=4, justify='right', state='readonly')
history_field.pack(ipady=5, fill='x')

# Configuración del marco de botones de la calculadora
btns_frame = tk.Frame(calc_frame)
btns_frame.pack(expand=True, fill='both')

# Datos de los botones de la calculadora
buttons_data = [
    ('C', 1, 0, 3, lambda: btn_clear()),
    ('/', 1, 3, 1, lambda: btn_click('/')),
    ('7', 2, 0, 1, lambda: btn_click(7)),
    ('8', 2, 1, 1, lambda: btn_click(8)),
    ('9', 2, 2, 1, lambda: btn_click(9)),
    ('*', 2, 3, 1, lambda: btn_click('*')),
    ('4', 3, 0, 1, lambda: btn_click(4)),
    ('5', 3, 1, 1, lambda: btn_click(5)),
    ('6', 3, 2, 1, lambda: btn_click(6)),
    ('-', 3, 3, 1, lambda: btn_click('-')),
    ('1', 4, 0, 1, lambda: btn_click(1)),
    ('2', 4, 1, 1, lambda: btn_click(2)),
    ('3', 4, 2, 1, lambda: btn_click(3)),
    ('+', 4, 3, 1, lambda: btn_click('+')),
    ('0', 5, 0, 2, lambda: btn_click(0)),
    ('.', 5, 2, 1, lambda: btn_click('.')),
    ('=', 5, 3, 1, lambda: btn_equal())
]

# Creación de los botones de la calculadora
for (text, row, col, colspan, command) in buttons_data:
    ttk.Button(btns_frame, text=text, command=command).grid(row=row, column=col, columnspan=colspan, sticky='nsew')
    if row < 5:
        btns_frame.grid_rowconfigure(row, weight=1)
    if col < 3:
        btns_frame.grid_columnconfigure(col, weight=1)

# Configuración inicial del marco de promedios ponderados
num_notas = tk.IntVar(value=6)
notas = [tk.StringVar() for _ in range(10)]
pesos = [tk.StringVar() for _ in range(10)]

weighted_avg_frame.pack_propagate(False)

ttk.Label(weighted_avg_frame, text="Número de Notas: ", font=('Arial', 14)).pack(side=tk.LEFT, padx=10, pady=10)
num_notas_menu = ttk.OptionMenu(weighted_avg_frame, num_notas, 6, *range(1, 11), command=lambda val: actualizar_campos(val))
num_notas_menu.pack(side=tk.LEFT, padx=10, pady=10)

notas_frame = tk.Frame(weighted_avg_frame)
notas_frame.pack(expand=True, fill='both', padx=20, pady=20)

ttk.Button(weighted_avg_frame, text="Calcular Promedio", command=calcular_promedio).pack(pady=10)
promedio_label = ttk.Label(weighted_avg_frame, text="Promedio Ponderado: ", font=('Arial', 14))
promedio_label.pack()

# Configuración del marco de gráficos
graph_frame = tk.Frame(root)

ttk.Label(graph_frame, text="Función", font=('Arial', 14)).pack(side=tk.TOP, padx=10, pady=10)
funcion_entry = tk.Entry(graph_frame, font=('Arial', 14))
funcion_entry.pack(side=tk.TOP, fill='x', padx=10, pady=10)

ttk.Button(graph_frame, text="Graficar", command=graficar_funcion).pack(side=tk.TOP, fill='x', padx=10, pady=10)
graph_result_label = ttk.Label(graph_frame, text="", font=('Arial', 14))
graph_result_label.pack(side=tk.TOP)

graph_plot_frame = tk.Frame(graph_frame)
graph_plot_frame.pack(expand=True, fill='both', padx=20, pady=20)

# Vincular eventos del teclado para la calculadora
root.bind('<Key>', on_key)

# Mostrar el modo inicial
change_mode("calculadora")

# Ejecutar el bucle principal
root.mainloop()
