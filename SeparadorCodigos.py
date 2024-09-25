import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import numpy as np

def dividir_codigos(codigos):
    if pd.isna(codigos):
        return [np.nan]
    if isinstance(codigos, int):  # Verificar si el código es un solo número
        return [codigos]
    if "-" in codigos:
        codigos_divididos = codigos.split("-")
        codigos_divididos = [int(c) if c.isdigit() else np.nan for c in codigos_divididos]
        return codigos_divididos
    else:
        codigos = codigos.split()
        codigos_divididos = [int(c) if c.isdigit() else np.nan for c in codigos]
        return codigos_divididos



# Función para previsualizar los primeros 10 valores del DataFrame
def previsualizar():
    if df is not None:
        mostrar_previsualizacion(df)
    else:
        messagebox.showerror("Error", "Por favor, primero procesa un archivo Excel.")
    
def mostrar_previsualizacion(df):
    top = tk.Toplevel()
    top.title("Previsualización del DataFrame")
    frame = tk.Frame(top)
    frame.pack(padx=10, pady=10)

    text = tk.Text(frame, wrap='none')
    scrollbar_y = tk.Scrollbar(frame, orient="vertical", command=text.yview)
    scrollbar_x = tk.Scrollbar(frame, orient="horizontal", command=text.xview)
    text.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    text.grid(row=0, column=0, sticky="nsew")
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    scrollbar_x.grid(row=1, column=0, sticky="ew")
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    text.insert(tk.END, df.to_string())
    text.config(state=tk.DISABLED)

# Función para procesar el archivo Excel
def procesar_excel():
    archivo = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx; *.xls")])
    if archivo:
        try:
            global df
            datos_excel = pd.read_excel(archivo)
            codigos_extraidos = datos_excel['Codebars'].apply(dividir_codigos)
            codigos_extraidos = pd.DataFrame(codigos_extraidos.tolist(), columns=[f"Codigo_{i+1}" for i in range(max(len(c) for c in codigos_extraidos))])
            df = pd.concat([datos_excel[['idproducto', 'Producto','visible','FechaUltimoPrecio','costo','Precio' ,'Codebar']], codigos_extraidos], axis=1)
            messagebox.showinfo("Éxito", "Se ha procesado el archivo Excel exitosamente.")
        except Exception as e:  
            print(f"Ocurrió un error al procesar el archivo: {str(e)}")


# Función para guardar el archivo Excel
def guardar_excel():
    if df is not None:
        ruta_nuevo_archivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if ruta_nuevo_archivo:
            try:
                df.to_excel(ruta_nuevo_archivo, index=False)
                messagebox.showinfo("Éxito", "Se ha guardado el archivo Excel exitosamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al guardar el archivo: {str(e)}")
    else:
        messagebox.showerror("Error", "No hay datos para guardar. Por favor, primero procesa un archivo Excel.")

# Crear la ventana principal
root = tk.Tk()
root.title("Procesador de Archivos Excel")
root.geometry("300x300")

# Botón para procesar el archivo Excel
procesar_button = ttk.Button(root, text="Procesar Archivo Excel", command=procesar_excel)
procesar_button.pack(pady=10)

# Botón para previsualizar los primeros 10 valores del DataFrame
previsualizar_button = ttk.Button(root, text="Previsualizar DataFrame", command=previsualizar)
previsualizar_button.pack(pady=10)

# Botón para guardar el archivo Excel
guardar_button = ttk.Button(root, text="Guardar Archivo Excel", command=guardar_excel)
guardar_button.pack(pady=10)

# DataFrame para almacenar los datos procesados
df = None

# Ejecutar la aplicación
root.mainloop()
