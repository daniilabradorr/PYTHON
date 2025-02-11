import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Conexión a la base de datos
try:
    conn = mysql.connector.connect(
        host='EJEMPLO',
        user='root',
        password='EJEMPLO.',
        database='gestion_empleados'
    )
except Exception as connect_err:
    print(f"Error en la conexión a la base de datos: {connect_err}")

# Inicialización de cursor
cursor = conn.cursor()

# Lectura del archivo Excel
tabla_excel = "C:/Users/Nitropc/Desktop/EJEMPLO"
tabla_empleados = pd.read_excel(f'{tabla_excel}/empleados_ejercicio.xlsx', header=0)
df_empleados = pd.DataFrame(tabla_empleados)

# Reemplazar valores inválidos
def reemplazar_valores_invalidos(df):
    return df.replace(['', None], 'N/A')

reemplazar_valores_invalidos(df_empleados)

# Función para actualizar salarios desde Excel
def actualizar_salarios_desde_excel(df_empleados):
    total_actualizados = 0
    total_empleados = len(df_empleados)

    try:
        for index, row in df_empleados.iterrows():
            id_empleado = row['id_empleado']
            nuevo_salario = row['salario']
            
            print(f"Procesando empleado con ID: {id_empleado} y salario: {nuevo_salario}")  # Depuración
            
            # Verificamos si el empleado existe en la base de datos
            check_query = "SELECT COUNT(1) FROM empleados WHERE id_empleado = %s"
            cursor.execute(check_query, (id_empleado,))
            existe = cursor.fetchone()[0]
            
            print(f"Empleado con ID {id_empleado} existe: {existe}")  # Depuración
            
            if existe:
                # Si el empleado existe, actualizamos el salario
                update_query = "UPDATE empleados SET salario = %s WHERE id_empleado = %s"
                cursor.execute(update_query, (nuevo_salario, id_empleado))
                total_actualizados += 1
                print(f"Salario actualizado para el empleado con ID: {id_empleado}")
            else:
                print(f"No se encontró un empleado con ID: {id_empleado}")
        
        # Confirmar cambios
        conn.commit()
        
        # Calcular el porcentaje de éxito
        porcentaje_exito = (total_actualizados / total_empleados) * 100
        return total_actualizados, porcentaje_exito

    except Exception as e:
        print(f"Error al actualizar los salarios: {e}")
        conn.rollback()

# Llamamos a la función para actualizar los salarios
total_actualizados, porcentaje_exito = actualizar_salarios_desde_excel(df_empleados)

# Cerrar conexión
conn.close()

# Graficar los resultados
def graficar_resultados(total_empleados, total_actualizados, porcentaje_exito):
    etiquetas = ['Actualizados', 'No Actualizados']
    valores = [total_actualizados, total_empleados - total_actualizados]

    plt.figure(figsize=(8, 6))
    plt.bar(etiquetas, valores, color=['green', 'red'])
    plt.title(f"Actualizaciones de Salarios\n{porcentaje_exito:.2f}% de éxito")
    plt.xlabel('Estado de Actualización')
    plt.ylabel('Número de Registros')
    plt.show()

# Graficar los resultados
graficar_resultados(len(df_empleados), total_actualizados, porcentaje_exito)
