from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from typing import List, Dict


def configurar_navegador() -> webdriver.Chrome:
    """
    Configura y devuelve un navegador Chrome en modo headless.

    Returns:
        webdriver.Chrome: Navegador Chrome configurado.
    """
    opciones = webdriver.ChromeOptions()
    opciones.add_argument('--headless')  # Ejecuta en modo headless (sin abrir la ventana del navegador)
    opciones.add_argument('--disable-gpu')
    opciones.add_argument('--no-sandbox')
    opciones.add_argument('--lang=en')

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opciones)


def extraer_categorias(navegador: webdriver.Chrome, url: str) -> List[Dict[str, str]]:
    """
    Extrae las categorías de productos desde una URL de Amazon.

    Args:
        navegador (webdriver.Chrome): Instancia del navegador.
        url (str): URL de la página de Amazon.

    Returns:
        List[Dict[str, str]]: Lista de diccionarios con nombres y alias de las categorías.
    """
    navegador.get(url)
    elementos_categoria = navegador.find_elements(By.CSS_SELECTOR, '#searchDropdownBox option')
    categorias = []
    for categoria in elementos_categoria:
        nombre_categoria = categoria.text.strip()  # Obtener el nombre de la categoría
        alias_categoria = categoria.get_attribute('value')  # Obtener el alias de la categoría
        if nombre_categoria and alias_categoria:
            # Limpiar el alias eliminando 'search-alias=' y cualquier otra parte irrelevante
            alias_limpio = alias_categoria.replace('search-alias=', '').strip()
            alias_espacio = alias_limpio.replace('-', ' ')  # Reemplazar guiones por espacios
            categorias.append({
                'nombre': nombre_categoria,
                'alias': alias_limpio,
                'alias2': alias_espacio
            })
    return categorias


def guardar_csv(categorias: List[Dict[str, str]], idioma: str) -> None:
    """
    Guarda las categorías en un archivo CSV.

    Args:
        categorias (List[Dict[str, str]]): Categorías extraídas.
        idioma (str): Idioma seleccionado (ingles o espanol).
    """
    # Crear un DataFrame de Pandas con los nombres y alias
    categorias_df = pd.DataFrame({
        'Nombre': [cat['nombre'] for cat in categorias],
        'Alias': [cat['alias'] for cat in categorias],
        'Alias2': [cat['alias2'] for cat in categorias]
    })

    # Guardar el DataFrame en un archivo CSV
    categorias_df.to_csv(f'categorias_amazon_{idioma}.csv', index=False)
    print(f"Categorías guardadas en 'categorias_amazon_{idioma}.csv'.")


def main() -> None:
    print("Ejecutandome")
    """
    Función principal que ejecuta el script.
    """
    # Seleccionar el idioma ('ingles' o 'espanol')
    idioma = 'ES'  # Cambiar a 'EN' o 'ES' según se requiera

    # Configurar el navegador
    navegador = configurar_navegador()

    # URL de Amazon según el idioma
    url = 'https://www.amazon.com/?language=en_US' if idioma == 'EN' else 'https://www.amazon.com/-/es/'

    # Extraer categorías de la página seleccionada
    categorias = extraer_categorias(navegador, url)
    print(f"Las categorias tienen este tipo {type(categorias)}")
    print(f"Estas son las categorias {categorias}")
    # Cerrar el navegador
    navegador.quit()

    # Guardar las categorías en un archivo CSV
    guardar_csv(categorias, idioma)
    
    return categorias

if __name__ == '__main__':
    main()