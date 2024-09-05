import pandas as pd
import numpy as np
import re

def limpiar_datos_csv(archivo_csv: str):
    df = pd.read_csv(archivo_csv, encoding='utf-8')

    # cambia estilo de nombre de columnas a snake_case
    def to_snake_case(name):
        name = re.sub(r'\s+', '_', name)
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        snake_case_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
        snake_case_name = snake_case_name.lower()
        snake_case_name = re.sub(r'__+', '_', snake_case_name)
        return snake_case_name

    # aplicar la funcion de cambio de estilo a las columnas del DataFrame
    df.columns = [to_snake_case(col) for col in df.columns]

    # manejo de valores nulos
    df = df.fillna('no hay historial')

    # monvertir tipos de datos numericos
    columnas_numericas = ['mas_bajo', 'mas_alto', 'actual', 'media']  
    df[columnas_numericas] = df[columnas_numericas].apply(pd.to_numeric, errors='coerce')

    archivo_limpio = archivo_csv.replace('.csv', '_limpio.csv')
    df.to_csv(archivo_limpio, index=False, encoding='utf-8')
    print(f"Archivo limpio guardado como {archivo_limpio}")

if __name__ == "__main__": 

    archivo_csv = 'historial_precios.csv'
    limpiar_datos_csv(archivo_csv)

    #dios sabe lo que luche con esta porqueria de scrip

