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

# Leer los datos desde un archivo Excel
ruta_archivo = 'ruta/al/archivo.xlsx'  # Reemplaza con la ruta de tu archivo Excel

# Leer los datos en un DataFrame desde la hoja 'Produccion' (puedes cambiar el nombre de la hoja si es necesario)
df_produccion = pd.read_excel(ruta_archivo, sheet_name='Produccion')

# Renombrar las columnas del DataFrame para que coincidan con las de la base de datos
df_produccion.rename(columns={
    'produccion_cantidad': 'cantidad_producida',
    'fecha_produccion': 'fecha'
}, inplace=True)

# Comprobamos los primeros datos para asegurarnos que se cargaron correctamente
print(df_produccion.head())

# Actualización de la cantidad producida en la base de datos
try:
    for index, row in df_produccion.iterrows():
        update_query = """
            UPDATE dbo.enunciado1_PROD
            SET cantidad_producida = ?
            WHERE id_produccion = ? AND fecha = ?
        """
        cursor.execute(update_query, row['cantidad_producida'], row['id_produccion'], row['fecha'])
    conn.commit()
    print("Registros de producción actualizados correctamente.")
except Exception as e:
    print(f"Error al actualizar los registros: {e}")
    conn.rollback()

conn.close()