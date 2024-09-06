import pandas as pd
import numpy as np
import re
from unidecode import unidecode

# Esta parte del código la tomé de Alexander
def limpiar_datos_excel(archivo_excel: str):
    df = pd.read_excel(archivo_excel)

    # Función para convertir nombres de columnas a snake_case
    def to_snake_case(name):
        name = re.sub(r'\s+', '_', name)
        name = re.sub(r'[^\w\s]', '', name)
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        snake_case_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
        snake_case_name = snake_case_name.lower()
        snake_case_name = re.sub(r'__+', '_', snake_case_name)
        return snake_case_name

    # Aplicar la función a las columnas del DataFrame
    df.columns = [to_snake_case(col) for col in df.columns]
    # Eliminar tildes y limpiar espacios
    df.columns = [unidecode(col).strip() for col in df.columns]  

    # Extraer valores numéricos de la columna 'vendidos_mes_pasado'
    extracted_values = df['vendidos_mes_pasado'].str.extract(r'(\d+\.?\d*)\s*(K)?\+')

    # Crear columna numérica con conversión de 'K' a miles
    df['vendidos_numerico'] = extracted_values.apply(
        lambda row: float(row[0]) * 1000 if row[1] == 'K' else (float(row[0]) if pd.notna(row[0]) else np.nan),
        axis=1
    )
    df['vendidos_numerico'] = df['vendidos_numerico'].astype('Int64')  # Convertir a entero

    # Eliminar columna 'precio_original'
    df = df.drop('precio_original', axis=1)

    # Limpiar la columna 'precio' y convertir a numérico
    df['precio'] = df['precio'].str.replace('US$', '', regex=False)
    df['precio'] = pd.to_numeric(df['precio'], errors='coerce')

    # Eliminar filas con valores nulos en 'num_de_calificaciones' y 'precio'
    df = df.dropna(subset=['num_de_calificaciones', 'precio'])
    df = df.reset_index(drop=True)

    # Arreglar valores en la columna 'tipo_de_precio'
    df['tipo_de_precio'] = df['tipo_de_precio'].replace({
        '3Âª Parte Nuevo': '3ª Parte Nuevo',
        '3Âª Parte Usado': '3ª Parte Usado'
    })

    # Guardar el archivo limpio
    archivo_limpio = archivo_excel.replace('.xlsx', '_limpio.xlsx')
    df.to_excel(archivo_limpio, index=False)
    print(f"Archivo limpio guardado como {archivo_limpio}")

# Me quedo pendiente saber como se llamaría el archivo que une los scrips
# Igual tomé la idea de Alexander
if __name__ == "__main__":
    archivo_excel = 'nombre_del_archivo_unido.xlsx'
    limpiar_datos_excel(archivo_excel)