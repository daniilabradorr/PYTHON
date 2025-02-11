import sqlite3
import os

# Clase Producto
class Producto:
    def __init__(self, nombre, categoria, cantidad, precio):
        self.nombre = nombre
        self.categoria = categoria
        self.cantidad = cantidad
        self.precio = precio

    def __str__(self):
        return f"Nombre: {self.nombre}, Categoría: {self.categoria}, Cantidad: {self.cantidad}, Precio: {self.precio}"

# Clase Inventario
class Inventario:
    def __init__(self, db_name="inventario.db"):
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.conexion = sqlite3.connect(self.db_path)
        self.cursor = self.conexion.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL
            )
        """)
        self.conexion.commit()

    def agregar_producto(self, producto):
        try:
            # Verificamos si ya existe un producto con el mismo nombre
            self.cursor.execute("SELECT * FROM productos WHERE nombre = ?", (producto.nombre,))
            if self.cursor.fetchone():
                print(f"El producto '{producto.nombre}' ya existe en la base de datos.")
                return

            # Insertamos el nuevo producto
            self.cursor.execute("""
                INSERT INTO productos (nombre, categoria, cantidad, precio)
                VALUES (?, ?, ?, ?)
            """, (producto.nombre, producto.categoria, producto.cantidad, producto.precio))
            self.conexion.commit()
            print(f"Producto '{producto.nombre}' agregado al inventario.")

        except sqlite3.Error as e:
            print(f"Error en la base de datos: {e}")

    def listar_productos(self):
        self.cursor.execute("SELECT * FROM productos")
        productos = self.cursor.fetchall()
        for prod in productos:
            print(f"ID: {prod[0]}, Nombre: {prod[1]}, Categoría: {prod[2]}, Cantidad: {prod[3]}, Precio: {prod[4]}")
        return productos

    def eliminar_producto(self, ID):
        try:
            self.cursor.execute("DELETE FROM productos WHERE ID = ?", (ID,))
            self.conexion.commit()
            print(f"Producto con ID {ID} eliminado de la base de datos.")
        except sqlite3.Error as e:
            print(f"Error en la base de datos: {e}")

    def actualizar_producto(self, ID, nombre=None, categoria=None, cantidad=None, precio=None):
        try:
            if nombre:
                self.cursor.execute("UPDATE productos SET nombre = ? WHERE ID = ?", (nombre, ID))
            if categoria:
                self.cursor.execute("UPDATE productos SET categoria = ? WHERE ID = ?", (categoria, ID))
            if cantidad:
                self.cursor.execute("UPDATE productos SET cantidad = ? WHERE ID = ?", (cantidad, ID))
            if precio:
                self.cursor.execute("UPDATE productos SET precio = ? WHERE ID = ?", (precio, ID))
            self.conexion.commit()
            print(f"Producto con ID {ID} actualizado.")
        except sqlite3.Error as e:
            print(f"Error en la base de datos: {e}")

    def exportar_inventario_txt(self, archivo="inventario.txt"):
        try:
            # Limpiamos el archivo antes de escribir en él
            with open(archivo, "w") as file:
                productos = self.listar_productos()
                for prod in productos:
                    file.write(f"ID: {prod[0]}, Nombre: {prod[1]}, Categoría: {prod[2]}, Cantidad: {prod[3]}, Precio: {prod[4]}\n")
            print(f"Inventario exportado a {archivo}.")
        except Exception as e:
            print(f"Error al exportar el inventario: {e}")

    def cerrar_conexion(self):
        self.conexion.close()

# Ejemplos de uso
if __name__ == "__main__":
    # Crear instancia de inventario
    inventario = Inventario()

    # Crear productos
    producto1 = Producto("Laptop", "Electrónica", 10, 999.99)
    producto2 = Producto("Teléfono", "Electrónica", 50, 499.99)

    # Agregar productos al inventario
    inventario.agregar_producto(producto1)
    inventario.agregar_producto(producto2)

    # Listar productos
    print("\nListado de productos:")
    inventario.listar_productos()

    # Actualizar un producto
    inventario.actualizar_producto(1, nombre="Laptop Gaming", precio=1299.99)

    # Listar productos actualizados
    print("\nProductos actualizados:")
    inventario.listar_productos()

    # Exportar inventario a archivo de texto
    inventario.exportar_inventario_txt()

    # Eliminar un producto
    inventario.eliminar_producto(2)

    # Listar productos tras eliminar
    print("\nProductos tras eliminación:")
    inventario.listar_productos()

    # Cerrar conexión a la base de datos
    inventario.cerrar_conexion()
