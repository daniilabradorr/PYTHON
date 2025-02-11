#Importar las librerias necesarias
import pandas as pd
import pyodbc
import numpy as np

#---------ESTO ES UN EJERCICIO TODOS LOS DATOS Y TABLAS SON FICTICIOS----------------------------
#---------ESTO ES UN EJERCICIO TODOS LOS DATOS Y TABLAS SON FICTICIOS----------------------------
#---------ESTO ES UN EJERCICIO TODOS LOS DATOS Y TABLAS SON FICTICIOS----------------------------

#Ruta de los archivos
Ruta_produccion = 'dsdasd'
Ruta_scrap = 'sdads'
Ruta_down = 'dsdsd'

#Lectura de los archivos
tabla_prod = pd.read_excel(f'{Ruta_produccion}/sdsadsads', header= 0)
tabla_scrap = pd.read_excel(f'{Ruta_scrap}/sdsadsads', header= 0)
tabla_down = pd.read_excel(f'{Ruta_down}/sdsadsads', header= 0)

#Inicializacion de cursor ,conn y comprobacion dataframe
cursor = None
conn = None
comprobacion_df = False

try:
    #Conexion a la base de datos
    conn= pyodbc.connect(
        "Driver={SQL Server};"
        "Server=hgfhhghgff;"
        "Database=jkhjkhjhjkh;"
        "Trusted_Connection=jhhjghjkgfgghj;"
    )
    try:
        #Creamos dataframes para realizar la comprobacion antes de tocar la base de datos
        df_prod = pd.DataFrame(tabla_prod)
        print(df_prod) #Para comprobar
        df_scrap = pd.DataFrame(tabla_scrap)
        print(df_scrap) #Para comprobar
        df_down = pd.DataFrame(tabla_down)
        print(df_down) #Para comprobar
    except Exception as df_err:
        print(f'Error al generar los dataframes: {df_err}')#Quiero poner un majeo de erro para fallo al crear un dataframe

    #Antes de pasar a la base de datos hacemos una comprobacion de los dataframes + pasar todos los valores vacios y nan a N/A
    def reemplazar_valores_invalidos(df):
        return df.replace(['', np.nan],'N/A')
    
    reemplazar_valores_invalidos(df_prod)
    reemplazar_valores_invalidos(df_scrap)
    reemplazar_valores_invalidos(df_down)
    
    #Comprobacion con cualquier if para ver que los dataframes estan tal y como queremos antes de tocar la BBDD
    if not df_prod.empty and not df_scrap.empty and df_down.empty:
        comprobacion_df = True
        print(f"Los DataFrames están correctamente llenos y listos para procesarse: {comprobacion_df}")
        comprobacion_df = True

        #Verificacion y creacion de las tablas
        def verificacion_y_creacion_tablas(conn,table_name, create_statement):
            cursor = conn.cursor()
            cursor.execuet(f"""IF OBJECT_ID('{table_name}', 'U' IS NOT NULL
                           BEGIN
                            DROP TABLE{table_name}
                            END
                            {create_statement})""")
        try:
            #Creacion de las TRES tablas
            verificacion_y_creacion_tablas(conn,'enunciado1_PROD',"""
                                            CREATE TABLE dbo.enunciado1_PROD(
                                            id_produccion INT PK,
                                            linea NVARCHAR(20),
                                            cantidad_producida INT,
                                            fecha DATE)""")
            verificacion_y_creacion_tablas(conn,'enunciado1_SCRAP',"""
                                            CREATE TABLE dbo.enunciado1_SCRAP(
                                            id_scrap INT PK,
                                            linea NVARCHAR(20),
                                            cantidad_defectuosa INT,
                                            causa NVARCHAR(50),
                                            fecha DATE)""")
            verificacion_y_creacion_tablas(conn,'enunciado1_DOWN',"""
                                            CREATE TABLE dbo.enunciado1_DOWN(
                                            id_down INT PK,
                                            linea NVARCHAR(20),
                                            tiempo_inactivo FLOAT,
                                            motivo NVARCHAR(50),
                                            fecha DATE)""")
        except Exception as create_err:
            print(f'Error al crear alguna tabla: {create_err}')
        
        #Insercion de datos a las tablas
        try:
            #insertar datos en tabla produccion
            for index, row in tabla_prod.iterrows():
                placeholders = ",".join(['?' for _ in tabla_prod.columns ])
                insert_query= f"""INSERT INTO dbo.enunciado1_PROD({','.join([f'[{col}]' for col in tabla_prod.columns])}) VALUES {placeholders}"""
                cursor.execute(insert_query, tuple(row))
        except pyodbc.error as insert_err:
            print(f"Error al insertar datos EN PROD | Error al insertar la fila {row.name}: {insert_err}")
            conn.rollback()
        #Confirmacion de la transaccion
        conn.commit()

        try:
            #insertar datos en tabla down
            for index, row in tabla_down.iterrows():
                placeholders = ",".join(['?' for _ in tabla_down.columns ])
                insert_query= f"""INSERT INTO dbo.enunciado1_DOWN({','.join([f'[{col}]' for col in tabla_down.columns])}) VALUES {placeholders}"""
                cursor.execute(insert_query, tuple(row))
        except pyodbc.error as insert_err:
            print(f"Error al insertar datos EN DOWN| Error al insertar la fila {row.name}: {insert_err}")
            conn.rollback()
        #Confirmacion de la transaccion
        conn.commit()

        try:
            #insertar datos en tabla scrap
            for index, row in tabla_scrap.iterrows():
                placeholders = ",".join(['?' for _ in tabla_scrap.columns ])
                insert_query= f"""INSERT INTO dbo.enunciado1_SCRAP({','.join([f'[{col}]' for col in tabla_scrap.columns])}) VALUES {placeholders}"""
                cursor.execute(insert_query, tuple(row))
        except pyodbc.error as insert_err:
            print(f"Error al insertar datos EN SCRAP| Error al insertar la fila {row.name}: {insert_err}")
            conn.rollback()
        #Confirmacion de la transaccion
        conn.commit()
    
        #CONSULTA , FALTA ESTA CONSULTA: Realiza una consulta que muestre la producción neta (producción - scrap) por línea de producción en cada fecha.
    

    else:
        comprobacion_df = False
        print(f"Error: Uno o más DataFrames están vacíos o contienen datos inválidos: {comprobacion_df}")    

#RESTO DE EXCEPTS PARA MANEJO DE ERRORES

except Exception as e:
    print(f'Error general: {e}')