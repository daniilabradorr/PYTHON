class Libro:
    def __init__(self, titulo, autor, isbn):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponible = True  # Por defecto, el libro está disponible

    def prestar(self):
        if self.disponible:
            self.disponible = False
            return True
        else:
            return False

    def devolver(self):
        if not self.disponible:
            self.disponible = True
            return True
        else:
            return False

    def __str__(self):
        estado = "Disponible" if self.disponible else "Prestado"
        return f"Libro: {self.titulo} - {self.autor} (ISBN: {self.isbn}) - Estado: {estado}"


class Usuario:
    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        self.id_usuario = id_usuario
        self.libros_prestados = []

    def tomar_prestado(self, libro):
        if len(self.libros_prestados) < 3:  # Máximo 3 libros por usuario
            self.libros_prestados.append(libro)
            return True
        else:
            return False

    def devolver_libro(self, libro):
        if libro in self.libros_prestados:
            self.libros_prestados.remove(libro)
            return True
        else:
            return False

    def __str__(self):
        libros_prestados_str = ", ".join([libro.titulo for libro in self.libros_prestados])
        return f"Usuario: {self.nombre} (ID: {self.id_usuario}) - Libros Prestados: {libros_prestados_str}"


class Biblioteca:
    def __init__(self):
        self.libros = []
        self.usuarios = []

    def agregar_libro(self, libro):
        self.libros.append(libro)

    def registrar_usuario(self, usuario):
        self.usuarios.append(usuario)

    def buscar_libro_por_isbn(self, isbn):
        for libro in self.libros:
            if libro.isbn == isbn:
                return libro
        return None

    def buscar_usuario_por_id(self, id_usuario):
        for usuario in self.usuarios:
            if usuario.id_usuario == id_usuario:
                return usuario
        return None

    def prestar_libro(self, isbn, id_usuario):
        libro = self.buscar_libro_por_isbn(isbn)
        usuario = self.buscar_usuario_por_id(id_usuario)

        if libro and usuario:
            if libro.disponible:
                if usuario.tomar_prestado(libro):
                    libro.prestar()
                    print(f"Libro '{libro.titulo}' prestado a {usuario.nombre}.")
                else:
                    print(f"El usuario {usuario.nombre} ya tiene el máximo de libros prestados.")
            else:
                print(f"El libro '{libro.titulo}' no está disponible.")
        else:
            print("Libro o usuario no encontrado.")

    def devolver_libro(self, isbn, id_usuario):
        libro = self.buscar_libro_por_isbn(isbn)
        usuario = self.buscar_usuario_por_id(id_usuario)

        if libro and usuario:
            if libro in usuario.libros_prestados:
                usuario.devolver_libro(libro)
                libro.devolver()
                print(f"Libro '{libro.titulo}' devuelto por {usuario.nombre}.")
            else:
                print(f"El usuario {usuario.nombre} no tiene prestado el libro '{libro.titulo}'.")
        else:
            print("Libro o usuario no encontrado.")

    def mostrar_estado(self):
        print("\n--- Estado de la Biblioteca ---")
        print("Libros en la biblioteca:")
        for libro in self.libros:
            print(libro)
        print("\nUsuarios registrados:")
        for usuario in self.usuarios:
            print(usuario)
        print("-------------------------------\n")


# Ejemplo de uso
if __name__ == "__main__":
    # Crear algunos libros
    libro1 = Libro("Cien años de soledad", "Gabriel García Márquez", "978-0307474728")
    libro2 = Libro("1984", "George Orwell", "978-0451524935")

    # Crear algunos usuarios
    usuario1 = Usuario("Juan Pérez", "001")
    usuario2 = Usuario("Ana Gómez", "002")

    # Crear la biblioteca
    biblioteca = Biblioteca()

    # Agregar libros a la biblioteca
    biblioteca.agregar_libro(libro1)
    biblioteca.agregar_libro(libro2)

    # Registrar usuarios en la biblioteca
    biblioteca.registrar_usuario(usuario1)
    biblioteca.registrar_usuario(usuario2)

    # Mostrar estado inicial
    biblioteca.mostrar_estado()

    # Prestar un libro a un usuario
    biblioteca.prestar_libro("978-0307474728", "001")

    # Mostrar estado después del préstamo
    biblioteca.mostrar_estado()

    # Devolver un libro
    biblioteca.devolver_libro("978-0307474728", "001")

    # Mostrar estado después de la devolución
    biblioteca.mostrar_estado()