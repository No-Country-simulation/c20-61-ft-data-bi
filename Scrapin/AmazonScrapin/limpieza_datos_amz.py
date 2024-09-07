import pandas as pd
import numpy as np
import re
import os
import sys

# Función para cambiar estilo de nombre de columnas a snake_case
def to_snake_case(name):
    name = re.sub(r'\s+', '_', name)
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    snake_case_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    snake_case_name = snake_case_name.lower()
    snake_case_name = re.sub(r'__+', '_', snake_case_name)
    return snake_case_name

def Clean():
    print("Empezando limpieza")
    # Ruta de la carpeta con los archivos .xlsx
    input_folder = './BasesDeDatos'
    output_folder = './BasesDeDatosLimpias'

    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Obtener lista de archivos .xlsx en la carpeta
    files = [f for f in os.listdir(input_folder) if f.endswith('.xlsx')]

    # Procesar cada archivo
    for file in files:
        print(f"Procesando archivo: {file}")
        file_path = os.path.join(input_folder, file)
        
        # Leer el archivo Excel
        df = pd.read_excel(file_path)
        
        # Se aplica la función de cambio de estilo a las columnas del df
        df.columns = [to_snake_case(col) for col in df.columns]
        
        # Eliminación de las columnas 'asin' y 'id'
        df = df.drop(['id'], axis=1, errors='ignore')
        
        # Limpiar columna de precio
        df['precio'] = pd.to_numeric(df['precio'].str.replace('US$', '', regex=False), errors='coerce')
        
        # Limpiar columna de calificación
        df['calificación'] = df['calificación'].str.extract(r'(\d+\.\d+)').astype(float)
        
        # Eliminar productos sin calificación
        df = df.dropna(subset=['num_de_calificaciones']).reset_index(drop=True)
        
        # Convertir a integer la columna 'num_de_calificaciones'
        df['num_de_calificaciones'] = df['num_de_calificaciones'].astype(int)
        
        # Limpiar columna 'vendidos_mes_pasado' y crear 'vendidos_numerico'
        extracted_values = df['vendidos_mes_pasado'].str.extract(r'(\d+\.?\d*)\s*(K)?\+')
        df['vendidos_numerico'] = extracted_values.apply(
            lambda row: float(row[0]) * 1000 if row[1] == 'K' else (float(row[0]) if pd.notna(row[0]) else np.nan),
            axis=1
        )
        
        # Guardar el archivo limpio en la carpeta de salida
        output_file = os.path.join(output_folder, file)
        df.to_excel(output_file, index=False)

    print("Limpieza de archivos completada.")