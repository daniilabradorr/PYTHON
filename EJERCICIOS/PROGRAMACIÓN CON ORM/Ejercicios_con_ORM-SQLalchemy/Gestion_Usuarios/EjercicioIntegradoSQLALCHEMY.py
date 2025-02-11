# ### **Ejercicio Integrado: Sistema de Gestión de Usuarios**
# El objetivo de este ejercicio es implementar un sistema básico de gestión de usuarios
# que permita realizar todas las operaciones CRUD.

from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Conexión a la base de datos
try:
    DATABASE_URL = f"mysql+pymysql://root:Dl16102003.@localhost:3306/gestion_empleados"
    engine = create_engine(DATABASE_URL, echo=True)  # `echo=True` muestra las consultas SQL generadas
    print("Conexión establecida con la Base de Datos")
except Exception as connect_err:
    print(f"Error al intentar conectar con la BBDD: {connect_err}")

# Declaramos tablas con Base (el esquema principal de SQLAlchemy)
Base = declarative_base()

# Modelo que define la tabla 'usuarios'
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True)  # ID único autoincremental
    nombre = Column(String(100), nullable=False)  # Campo obligatorio
    edad = Column(Integer, nullable=False)  # Campo obligatorio
    email = Column(String(100), unique=True, nullable=False)  # Campo único y obligatorio

# Crear las tablas en la base de datos
try:
    Base.metadata.create_all(engine)
    print("Tablas creadas con éxito")
except Exception as create_tables_err:
    print(f"Error al crear las tablas: {create_tables_err}")

# Iniciamos sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()

# Funciones CRUD (Create, Read, Update, Delete)
def crear_usuario(nombre, edad, email):
    """Crea un nuevo usuario en la base de datos."""
    if edad < 0:
        print("La edad debe ser positiva.")
        return
    if not "@" in email:
        print("El email no es válido.")
        return
    usuario = Usuario(nombre=nombre, edad=edad, email=email)
    session.add(usuario)  # Agrega el usuario a la sesión
    session.commit()  # Guarda los cambios en la base de datos
    print(f"Usuario creado: {usuario.nombre} (ID: {usuario.id})")

#Crear usuarios masivamente
def crear_usuarios_masivamente(lista_usuarios):
    """
    Crea múltiples usuarios en la base de datos.
    :param lista_usuarios: Lista de diccionarios con los datos de cada usuario.
    """
    usuarios_a_agregar = []
    for datos in lista_usuarios:
        nombre = datos.get("nombre")
        edad = datos.get("edad")
        email = datos.get("email")
        if edad < 0:
            print(f"La edad debe ser positiva. Usuario omitido: {nombre}")
            continue
        if "@" not in email:
            print(f"El email no es válido. Usuario omitido: {nombre}")
            continue
        usuario = Usuario(nombre=nombre, edad=edad, email=email)
        usuarios_a_agregar.append(usuario)
    if usuarios_a_agregar:
        session.bulk_save_objects(usuarios_a_agregar)  # Agrega múltiples objetos a la vez
        session.commit()
        print(f"{len(usuarios_a_agregar)} usuarios creados exitosamente.")
    else:
        print("No se crearon usuarios debido a errores en los datos.")


def listar_usuarios(filtro=None):
    """Lista todos los usuarios o aplica un filtro."""
    if filtro:
        usuarios = session.query(Usuario).filter(filtro).all()
    else:
        usuarios = session.query(Usuario).all()
    if usuarios:
        for usuario in usuarios:
            print(f"ID: {usuario.id}, Nombre: {usuario.nombre}, Edad: {usuario.edad}, Email: {usuario.email}")
    else:
        print("No se encontraron usuarios.")

def actualizar_usuario(usuario_id, **kwargs):
    """Actualiza los datos de un usuario existente."""
    usuario = session.query(Usuario).filter_by(id=usuario_id).first()
    if not usuario:
        print("Usuario no encontrado.")
        return
    for attr, value in kwargs.items():
        setattr(usuario, attr, value)  # Actualiza los atributos dinámicamente
    session.commit()
    print(f"Usuario actualizado: ID: {usuario.id}, Nombre: {usuario.nombre}")

def eliminar_usuario(usuario_id=None, filtro=None):
    """Elimina un usuario por ID o con un filtro."""
    if usuario_id:
        usuario = session.query(Usuario).filter_by(id=usuario_id).first()
        if usuario:
            session.delete(usuario)  # Marca el usuario para eliminar
            session.commit()  # Aplica el cambio en la base de datos
            print(f"Usuario eliminado: {usuario.nombre}")
        else:
            print("Usuario no encontrado.")
    elif filtro:
        usuarios = session.query(Usuario).filter(filtro).all()
        if usuarios:
            for usuario in usuarios:
                session.delete(usuario)
            session.commit()
            print(f"Usuarios eliminados: {len(usuarios)}")
        else:
            print("No se encontraron usuarios que coincidan con el filtro.")

#Eliminar usuarios de manera masiva por IDs o filtro
def eliminar_usuarios_masivamente(lista_ids=None, filtro=None):
    """
    Elimina múltiples usuarios según una lista de IDs o un filtro.
    :param lista_ids: Lista de IDs de los usuarios a eliminar.
    :param filtro: Filtro SQLAlchemy para seleccionar usuarios.
    """
    if lista_ids:
        usuarios = session.query(Usuario).filter(Usuario.id.in_(lista_ids)).all()
    elif filtro:
        usuarios = session.query(Usuario).filter(filtro).all()
    else:
        print("No se especificaron IDs o filtro para eliminar usuarios.")
        return

    if usuarios:
        for usuario in usuarios:
            session.delete(usuario)
        session.commit()
        print(f"{len(usuarios)} usuarios eliminados exitosamente.")
    else:
        print("No se encontraron usuarios para eliminar.")


def generar_reporte():
    """Genera un informe con el total de usuarios y el promedio de edades."""
    total_usuarios = session.query(Usuario).count()  # Cuenta el total de usuarios
    promedio_edad = session.query(func.avg(Usuario.edad)).scalar()  # Promedio de edad
    print(f"Total de usuarios: {total_usuarios}")
    if promedio_edad:
        print(f"Promedio de edad: {promedio_edad:.2f}")
    else:
        print("No hay usuarios registrados.")

# Menú interactivo
if __name__ == "__main__":
    while True:
        print("\n--- Menú de Gestión de Usuarios ---")
        print("1. Crear usuario")
        print("2. Listar usuarios")
        print("3. Actualizar usuario")
        print("4. Eliminar usuario")
        print("5. Generar reporte")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Ingrese el nombre del usuario: ")
            edad = int(input("Ingrese la edad del usuario: "))
            email = input("Ingrese el email del usuario: ")
            crear_usuario(nombre, edad, email)

        elif opcion == "2":
            print("Listado de usuarios:")
            listar_usuarios()

        elif opcion == "3":
            usuario_id = int(input("Ingrese el ID del usuario a actualizar: "))
            nombre = input("Nuevo nombre (dejar vacío para no cambiar): ")
            edad = input("Nueva edad (dejar vacío para no cambiar): ")
            email = input("Nuevo email (dejar vacío para no cambiar): ")
            cambios = {}
            if nombre:
                cambios["nombre"] = nombre
            if edad:
                cambios["edad"] = int(edad)
            if email:
                cambios["email"] = email
            actualizar_usuario(usuario_id, **cambios)

        elif opcion == "4":
            usuario_id = int(input("Ingrese el ID del usuario a eliminar: "))
            eliminar_usuario(usuario_id=usuario_id)

        elif opcion == "5":
            print("Reporte de usuarios:")
            generar_reporte()

        elif opcion == "6":
            print("Saliendo del sistema.")
            break
        
        elif opcion == "7":
            print("Crear usuarios masivamente")
            n = int(input("¿Cuántos usuarios desea agregar? "))
            lista_usuarios = []
            for _ in range(n):
                nombre = input("Ingrese el nombre del usuario: ")
                edad = int(input("Ingrese la edad del usuario: "))
                email = input("Ingrese el email del usuario: ")
                lista_usuarios.append({"nombre": nombre, "edad": edad, "email": email})
            crear_usuarios_masivamente(lista_usuarios)

        elif opcion == "8":
            print("Eliminar usuarios masivamente")
            print("1. Eliminar por lista de IDs")
            print("2. Eliminar por filtro")
            subopcion = input("Seleccione una opción: ")
            if subopcion == "1":
                lista_ids = list(map(int, input("Ingrese los IDs separados por coma: ").split(",")))
                eliminar_usuarios_masivamente(lista_ids=lista_ids)
            elif subopcion == "2":
                print("Ejemplo de filtro: Usuario.edad > 50")
                filtro = eval(input("Ingrese el filtro para eliminar usuarios: "))
                eliminar_usuarios_masivamente(filtro=filtro)
            else:
                print("Opción no válida.")

        else:
            print("Opción no válida. Intente nuevamente.")
