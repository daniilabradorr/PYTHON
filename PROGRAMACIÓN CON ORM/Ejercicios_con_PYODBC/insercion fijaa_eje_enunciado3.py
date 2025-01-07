import pyodbc
import pandas as pd

# Conexión a la base de datos
conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=tu_servidor;"  # Asegúrate de reemplazar esto con tu servidor
    "Database=tu_base_de_datos;"  # Asegúrate de reemplazar esto con tu base de datos
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

# Leer datos desde un archivo Excel
ruta_archivo = 'ruta/al/archivo_empleados.xlsx'  # Reemplaza con la ruta de tu archivo Excel
df_empleados = pd.read_excel(ruta_archivo)

# Comprobamos los primeros datos para asegurarnos que se cargaron correctamente
print(df_empleados.head())

# Inserción de los datos en la tabla empleados
try:
    for index, row in df_empleados.iterrows():
        # La consulta SQL usa placeholders (?) para evitar concatenación directa de valores
        insert_query = """
            INSERT INTO dbo.empleados (id_empleado, nombre, apellido, fecha_ingreso, salario)
            VALUES (?, ?, ?, ?, ?)
        """
        
        # Ejecutamos la consulta con los valores de la fila actual del DataFrame
        cursor.execute(insert_query, row['id_empleado'], row['nombre'], row['apellido'], row['fecha_ingreso'], row['salario'])
    
    conn.commit()
    print("Datos de empleados insertados correctamente.")
except Exception as e:
    print(f"Error al insertar los datos: {e}")
    conn.rollback()

conn.close()
