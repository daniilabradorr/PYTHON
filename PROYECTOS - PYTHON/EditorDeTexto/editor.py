import tkinter as tk  # Importamos Tkinter para crear la interfaz gráfica
from tkinter import filedialog, messagebox, PhotoImage  # Importamos funciones para diálogos de archivos y mensajes

# Creamos la ventana principal de la aplicación
root = tk.Tk()
root.title("Editor de Texto")  # Establecemos el título de la ventana
root.geometry("1000x800")  # Definimos el tamaño inicial de la ventana

# Establecemos el icono de la ventana
root.iconbitmap("img/icono.ico")

# Cargamos y redimensionamos la imagen del logo
image = PhotoImage(file="img/logo.png")
image_resized = image.subsample(4, 4)  # Reduzco el tamaño de la imagen
image_label = tk.Label(root, image=image_resized)  # Creamos un label con la imagen
image_label.pack(padx=10, pady=10)  # Posicionamos la imagen en la ventana

# Creamos el área de texto con una barra de desplazamiento
txt_frame = tk.Frame(root)  # Marco contenedor para organizar elementos
txt_frame.pack(fill="both", expand=True, padx=10, pady=10)  # Expande el área de texto

text_area = tk.Text(txt_frame, wrap="word", bg="white", fg="black", font=("Arial", 12))  # Definimos el área de texto
scrollbar = tk.Scrollbar(txt_frame, command=text_area.yview)  # Agregamos barra de desplazamiento
text_area.config(yscrollcommand=scrollbar.set)

text_area.pack(side="left", fill="both", expand=True)  # Ubicamos el área de texto
scrollbar.pack(side="right", fill="y")  # Ubicamos la barra de desplazamiento

# Creamos la barra de menú
menu_barra = tk.Menu(root)
root.config(menu=menu_barra)

# Variable para almacenar la ruta del archivo actual
current_file = None

# Función para crear un nuevo archivo
def new_file():
    global current_file
    text_area.delete(1.0, tk.END)  # Borra todo el contenido del área de texto
    current_file = None  # Restablecemos la ruta del archivo actual

# Función para abrir un archivo existente
def open_file():
    global current_file
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            text_area.delete(1.0, tk.END)  # Borra contenido previo
            text_area.insert(tk.END, file.read())  # Carga el contenido del archivo
            current_file = file_path  # Guarda la ruta del archivo abierto

# Función para guardar el archivo actual
def save_file():
    global current_file
    if current_file:
        with open(current_file, "w") as file:
            file.write(text_area.get(1.0, tk.END))  # Guarda el contenido actual
    else:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(text_area.get(1.0, tk.END))
            current_file = file_path  # Guarda la nueva ruta del archivo

# Función para salir de la aplicación
def exit_editor():
    if messagebox.askokcancel("Salir", "¿Seguro que quieres salir?"):
        root.destroy()  # Cierra la aplicación

# Agregamos opciones al menú "Archivo"
file_menu = tk.Menu(menu_barra, tearoff=0)
file_menu.add_command(label="Nuevo", command=new_file)
file_menu.add_command(label="Abrir", command=open_file)
file_menu.add_command(label="Guardar", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Salir", command=exit_editor)
menu_barra.add_cascade(label="Archivo", menu=file_menu)

# Botón para guardar el archivo
guardar_btn = tk.Button(root, text="Guardar", command=save_file, font=("Arial", 12, "bold"), fg="white", bg="#28a745", padx=10, pady=5)
guardar_btn.pack(side="right", padx=20, pady=10)

# Función para cambiar el tamaño de la fuente
def change_font_size(size):
    try:
        text_area.tag_add("selected", tk.SEL_FIRST, tk.SEL_LAST)
        text_area.tag_configure("selected", font=("Arial", size))
    except tk.TclError:
        pass  # Evita errores si no hay texto seleccionado

# Función para disminuir el tamaño de la fuente
def decrease_font_size():
    try:
        current_font = text_area.tag_cget("selected", "font")
        current_size = int(current_font.split()[1])
        new_size = max(current_size - 2, 8)  # Tamaño mínimo de 8
        text_area.tag_configure("selected", font=("Arial", new_size))
    except tk.TclError:
        pass

# Función para alternar negrita
def toggle_bold():
    try:
        current_font = text_area.tag_cget("selected", "font")
        if "bold" in current_font:
            text_area.tag_configure("selected", font=("Arial", 12))
        else:
            text_area.tag_configure("selected", font=("Arial", 12, "bold"))
    except tk.TclError:
        pass

# Función para alternar cursiva
def toggle_italic():
    try:
        current_font = text_area.tag_cget("selected", "font")
        if "italic" in current_font:
            text_area.tag_configure("selected", font=("Arial", 12))
        else:
            text_area.tag_configure("selected", font=("Arial", 12, "italic"))
    except tk.TclError:
        pass

# Botones para modificar formato del texto
font_size_btn = tk.Button(root, text="Aumentar tamaño", command=lambda: change_font_size(16), font=("Arial", 12, "bold"), fg="white", bg="black", padx=10, pady=5)
font_size_btn.pack(side="left", padx=20, pady=10)

decrease_font_btn = tk.Button(root, text="Disminuir tamaño", command=decrease_font_size, font=("Arial", 12, "bold"), fg="white", bg="black", padx=10, pady=5)
decrease_font_btn.pack(side="left", padx=20, pady=10)

bold_btn = tk.Button(root, text="Negrita", command=toggle_bold, font=("Arial", 12, "bold"), fg="white", bg="#007bff", padx=10, pady=5)
bold_btn.pack(side="left", padx=20, pady=10)

italic_btn = tk.Button(root, text="Cursiva", command=toggle_italic, font=("Arial", 12, "bold"), fg="white", bg="#ffc107", padx=10, pady=5)
italic_btn.pack(side="left", padx=20, pady=10)

# Inicio del bucle principal de la aplicación
root.mainloop()