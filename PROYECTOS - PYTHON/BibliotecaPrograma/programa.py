import sqlite3
import tkinter as tk
from tkinter import messagebox

class Biblioteca:
    def __init__(self):
        self.conn = sqlite3.connect('biblioteca.db')
        self.cursor = self.conn.cursor()
        
        # Crear tabla para libros
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS libros
                               (titulo TEXT, autor TEXT, isbn TEXT, estado TEXT)''')
        
        # Crear tabla para lectores
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS lectores
                               (nombre TEXT)''')
        
        # Crear tabla para préstamos
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS prestamos
                               (isbn TEXT, lector TEXT, fecha TEXT)''')
        
        self.conn.commit()

    def añadir_libro(self, titulo, autor, isbn):
        self.cursor.execute('INSERT INTO libros VALUES (?, ?, ?, ?)', 
                            (titulo, autor, isbn, 'disponible'))
        self.conn.commit()

    def añadir_lector(self, nombre):
        self.cursor.execute('INSERT INTO lectores VALUES (?)', (nombre,))
        self.conn.commit()

    def buscar_libro_por_titulo(self, titulo):
        self.cursor.execute('SELECT * FROM libros WHERE titulo LIKE ?', (f'%{titulo}%',))
        return self.cursor.fetchall()

    def listar_libros(self):
        self.cursor.execute('SELECT * FROM libros')
        return self.cursor.fetchall()

    def listar_lectores(self):
        self.cursor.execute('SELECT * FROM lectores')
        return self.cursor.fetchall()

    def prestar_libro(self, isbn, lector, fecha):
        # Verificar disponibilidad del libro
        self.cursor.execute('SELECT estado FROM libros WHERE isbn = ?', (isbn,))
        resultado = self.cursor.fetchone()
        if resultado and resultado[0] == 'disponible':
            # Actualizar estado del libro y registrar el préstamo
            self.cursor.execute('UPDATE libros SET estado = ? WHERE isbn = ?', ('prestado', isbn))
            self.cursor.execute('INSERT INTO prestamos VALUES (?, ?, ?)', (isbn, lector, fecha))
            self.conn.commit()
            return True
        return False

    def devolver_libro(self, isbn):
        # Verificar si el libro está prestado
        self.cursor.execute('SELECT estado FROM libros WHERE isbn = ?', (isbn,))
        resultado = self.cursor.fetchone()
        if resultado and resultado[0] == 'prestado':
            # Actualizar estado del libro y eliminar el préstamo
            self.cursor.execute('UPDATE libros SET estado = ? WHERE isbn = ?', ('disponible', isbn))
            self.cursor.execute('DELETE FROM prestamos WHERE isbn = ?', (isbn,))
            self.conn.commit()
            return True
        return False


class BibliotecaApp:
    def __init__(self, root, biblioteca):
        self.biblioteca = biblioteca
        self.root = root
        self.root.title("Biblioteca")

        # Frame principal
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        # Botones principales
        self.btn_añadir_libro = tk.Button(self.frame, text="Añadir Libro", command=self.ventana_añadir_libro)
        self.btn_añadir_libro.grid(row=0, column=0, padx=10)

        self.btn_añadir_lector = tk.Button(self.frame, text="Añadir Lector", command=self.ventana_añadir_lector)
        self.btn_añadir_lector.grid(row=0, column=1, padx=10)

        self.btn_prestar_libro = tk.Button(self.frame, text="Prestar Libro", command=self.ventana_prestar_libro)
        self.btn_prestar_libro.grid(row=0, column=2, padx=10)

        self.btn_devolver_libro = tk.Button(self.frame, text="Devolver Libro", command=self.ventana_devolver_libro)
        self.btn_devolver_libro.grid(row=0, column=3, padx=10)

        self.btn_listar_libros = tk.Button(self.frame, text="Listar Libros", command=self.listar_libros)
        self.btn_listar_libros.grid(row=0, column=4, padx=10)

        # Área de resultados
        self.resultado = tk.Text(root, height=15, width=80)
        self.resultado.pack(pady=10)

    def ventana_añadir_libro(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Añadir Libro")
        
        # Campos para añadir libro
        tk.Label(ventana, text="Título:").grid(row=0, column=0, padx=10, pady=5)
        titulo_entry = tk.Entry(ventana)
        titulo_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(ventana, text="Autor:").grid(row=1, column=0, padx=10, pady=5)
        autor_entry = tk.Entry(ventana)
        autor_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(ventana, text="ISBN:").grid(row=2, column=0, padx=10, pady=5)
        isbn_entry = tk.Entry(ventana)
        isbn_entry.grid(row=2, column=1, padx=10, pady=5)

        def guardar_libro():
            titulo = titulo_entry.get()
            autor = autor_entry.get()
            isbn = isbn_entry.get()
            if titulo and autor and isbn:
                self.biblioteca.añadir_libro(titulo, autor, isbn)
                messagebox.showinfo("Éxito", "Libro añadido correctamente.")
                ventana.destroy()
            else:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")

        tk.Button(ventana, text="Guardar", command=guardar_libro).grid(row=3, column=0, columnspan=2, pady=10)

    def ventana_añadir_lector(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Añadir Lector")
        
        # Campos para añadir lector
        tk.Label(ventana, text="Nombre del Lector:").grid(row=0, column=0, padx=10, pady=5)
        lector_entry = tk.Entry(ventana)
        lector_entry.grid(row=0, column=1, padx=10, pady=5)

        def guardar_lector():
            nombre = lector_entry.get()
            if nombre:
                self.biblioteca.añadir_lector(nombre)
                messagebox.showinfo("Éxito", "Lector añadido correctamente.")
                ventana.destroy()
            else:
                messagebox.showerror("Error", "El campo de nombre es obligatorio.")

        tk.Button(ventana, text="Guardar", command=guardar_lector).grid(row=1, column=0, columnspan=2, pady=10)

    def ventana_prestar_libro(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Prestar Libro")

        tk.Label(ventana, text="ISBN:").grid(row=0, column=0, padx=10, pady=5)
        isbn_entry = tk.Entry(ventana)
        isbn_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(ventana, text="Lector:").grid(row=1, column=0, padx=10, pady=5)
        lector_entry = tk.Entry(ventana)
        lector_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(ventana, text="Fecha (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5)
        fecha_entry = tk.Entry(ventana)
        fecha_entry.grid(row=2, column=1, padx=10, pady=5)

        def prestar():
            isbn = isbn_entry.get()
            lector = lector_entry.get()
            fecha = fecha_entry.get()
            if isbn and lector and fecha:
                if self.biblioteca.prestar_libro(isbn, lector, fecha):
                    messagebox.showinfo("Éxito", "Libro prestado correctamente.")
                else:
                    messagebox.showerror("Error", "El libro no está disponible.")
                ventana.destroy()
            else:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")

        tk.Button(ventana, text="Prestar", command=prestar).grid(row=3, column=0, columnspan=2, pady=10)

    def ventana_devolver_libro(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Devolver Libro")

        tk.Label(ventana, text="ISBN:").grid(row=0, column=0, padx=10, pady=5)
        isbn_entry = tk.Entry(ventana)
        isbn_entry.grid(row=0, column=1, padx=10, pady=5)

        def devolver():
            isbn = isbn_entry.get()
            if isbn:
                if self.biblioteca.devolver_libro(isbn):
                    messagebox.showinfo("Éxito", "Libro devuelto correctamente.")
                else:
                    messagebox.showerror("Error", "El libro no está prestado.")
                ventana.destroy()
            else:
                messagebox.showerror("Error", "El campo ISBN es obligatorio.")

        tk.Button(ventana, text="Devolver", command=devolver).grid(row=1, column=0, columnspan=2, pady=10)

    def listar_libros(self):
        libros = self.biblioteca.listar_libros()
        self.resultado.delete(1.0, tk.END)
        for libro in libros:
            self.resultado.insert(tk.END, f"Título: {libro[0]}, Autor: {libro[1]}, ISBN: {libro[2]}, Estado: {libro[3]}\n")


# Crear instancia de Biblioteca
biblioteca = Biblioteca()

# Iniciar la interfaz gráfica
root = tk.Tk()
app = BibliotecaApp(root, biblioteca)
root.mainloop()
