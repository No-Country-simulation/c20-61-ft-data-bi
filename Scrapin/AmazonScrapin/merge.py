import os
import pandas as pd

def concatenar_excel_con_nombre_directorio(directorio_entrada, archivo_salida):
    # Crear una lista para almacenar los DataFrames
    dataframes = []

    # Verificar si el directorio existe
    if not os.path.exists(directorio_entrada):
        print(f"El directorio {directorio_entrada} no existe.")
        return

    # Recorrer todos los archivos en el directorio de entrada
    for archivo in os.listdir(directorio_entrada):
        if archivo.endswith('.xlsx'):
            ruta_archivo = os.path.join(directorio_entrada, archivo)

            # Cargar el archivo Excel en un DataFrame
            df = pd.read_excel(ruta_archivo)

            # Agregar una columna con el nombre del archivo (sin la extensión)
            df['nombre_origen'] = os.path.splitext(archivo)[0]

            # Agregar el DataFrame a la lista
            dataframes.append(df)

    # Concatenar todos los DataFrames en uno solo
    df_concatenado = pd.concat(dataframes, ignore_index=True)

    # Reorganizar las columnas para que 'nombre_origen' sea la primera columna
    columnas = ['nombre_origen'] + [col for col in df_concatenado.columns if col != 'nombre_origen']
    df_concatenado = df_concatenado[columnas]

    # Guardar el DataFrame concatenado en un nuevo archivo Excel
    df_concatenado.to_excel(archivo_salida, index=False)
    print(f"Archivos concatenados y guardados en {archivo_salida}")

# Especifica las rutas del directorio de entrada y el archivo de salida
directorio_entrada = 'BasesDeDatosLimpias'
archivo_salida = 'df_concatenado.xlsx'

# Ejecutar la función
concatenar_excel_con_nombre_directorio(directorio_entrada, archivo_salida)