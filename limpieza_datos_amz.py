import pandas as pd
import numpy as np
import re
import os
import sys

sys.path.append(os.getcwd())

# Colocar el nombre del archivo a limpiar
df = pd.read_excel('Ropa deportiva.xlsx')

# Función para cambiar estilo de nombre de columnas a snake_case


def to_snake_case(name):
    name = re.sub(r'\s+', '_', name)

    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    snake_case_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    snake_case_name = snake_case_name.lower()
    snake_case_name = re.sub(r'__+', '_', snake_case_name)

    return snake_case_name


# Se aplica la función de cambio de estilo a las columnas del df
df.columns = [to_snake_case(col) for col in df.columns]

# Eliminación de las columnas ASIN y ID

df = df.drop(['asin', 'id'], axis=1)

# Podría agregarse a la eliminación 'precio_original'
# df = df.drop(['asin','precio_original'], axis=1)

# Se limpia columna de precio
df['precio'] = pd.to_numeric(df['precio'].str.replace(
    'US$', '', regex=False), errors='coerce')

# Se limpia columna de calificación
df['calificación'] = df['calificación'].str.extract(
    r'(\d+\.\d+)').astype(float)

# Productos sin calificación se eliminan
df = df.dropna(subset=['num_de_calificaciones']).reset_index(drop=True)

# Se convierte a integer columna 'num_de_calificaciones'
df['num_de_calificaciones'] = df['num_de_calificaciones'].astype(int)

# Se limpia columna 'vendidos_mes_pasado'y se crea 'vendidos_numerico'
extracted_values = df['vendidos_mes_pasado'].str.extract(
    r'(\d+\.?\d*)\s*(K)?\+')

df['vendidos_numerico'] = extracted_values.apply(
    lambda row: float(
        row[0]) * 1000 if row[1] == 'K' else (float(row[0]) if pd.notna(row[0]) else np.nan),
    axis=1
)

# Eliminación de posibles duplicados
df = df.drop_duplicates()

# Eliminación de productos sin precio, debido a que son productos multi selección
df = df.dropna(subset=['precio'])


# Exporta resultados a excel
df.to_excel('archivo_limpio.xlsx', index=False)
