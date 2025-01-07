# Importación de las clases necesarias de SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Boolean, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Declarando la base para todos los modelos
Base = declarative_base()

# Definición del modelo de la clase 'Producto'
class Producto(Base):  # Clase que representa un producto en la base de datos
    __tablename__ = "productos"  # Nombre de la tabla en la base de datos

    # Definición de las columnas de la tabla 'productos'
    id = Column(Integer, primary_key=True, autoincrement=True)  
    nombre = Column(String(255), nullable=False)  
    tipo = Column(String(255), nullable=False)  
    precio = Column(Float, nullable=False) 
    disponible = Column(Boolean, default=True) 

    def __repr__(self):  # Método que define cómo se muestra un objeto 'Producto'
        # Cuando se imprime el objeto, muestra los valores de las propiedades de manera legible
        print(f"Producto: id-{self.id}, nombre-{self.nombre}, tipo-{self.tipo}, precio-{self.precio}, disponible-{self.disponible}")


# Configuración de la conexión a la base de datos
try:
    # IMPORTANTE: Es recomendable no incluir la contraseña directamente en el código para proyectos reales, sino usar un archivo .env
    DATABASE_URL = f"EJEMPLO"  # URL para conectar con la base de datos 'restaurante'
    
    # Creación del motor de conexión con la base de datos usando la URL proporcionada
    engine = create_engine(DATABASE_URL, echo=True)  # `echo=True` muestra las consultas SQL generadas en la consola para depuración
    print("Conexión establecida con la Base de Datos")  # Mensaje si la conexión es exitosa
except Exception as connect_err:
    print(f"Error al intentar conectar con la BBDD: {connect_err}")


# Creación de todas las tablas definidas por las clases que heredan de 'Base'
# Si la tabla 'productos' no existe, se crea. Esto se realiza con la metadata de Base
Base.metadata.create_all(engine)  # Crea las tablas en la base de datos asociada con 'engine'

# Se configura la clase 'Session' que se usará para interactuar con la base de datos
Session = sessionmaker(bind=engine)  # 'sessionmaker' crea una clase de sesión configurada con el motor 'engine'
