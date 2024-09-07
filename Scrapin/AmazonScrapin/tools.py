import re
import sys
import random
import pandas as pd
import os
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrighTimeoutError

def tiempoAlea(val):
    ranges = [i for i in range(3, val + 1)]
    return random.choice(ranges)

def agenteUsuario():
    with open("user-agents.txt") as f:
        agente = f.read().split("\n")
        return random.choice(agente)

class TryExcept:
    def text(self, element):
        try:
            return element.inner_text().strip()
        except AttributeError:
            return "Sin información"

    def attributes(self, element, attr):
        try:
            return element.get_attribute(attr)
        except AttributeError:
            return "Valor no disponible"

def scraping(head,produbuscar):
    datosAmazon = []
    catchClause = TryExcept()

    produbusner = produbuscar.replace(" ", "+")
    ingresoProducto = f"https://www.amazon.com/s?k={produbusner}&language=es_US"

    amazon_link_pattern = re.search(r"https://www.amazon.com/s\?.+", ingresoProducto)
    if amazon_link_pattern is None:
        print(f"Enlace no válido. Ingrese un enlace de Amazon que incluya la categoría de producto de su elección.")
        sys.exit()

    try:
        with sync_playwright() as play:
            navegador = play.chromium.launch(headless=head, slow_mo=3 * 1000)
            pagina = navegador.new_page(user_agent=agenteUsuario())
            pagina.goto(ingresoProducto)

            pagina.wait_for_timeout(timeout=tiempoAlea(4) * 1000)

            contenidoPrincipal = "//div[@data-component-type='s-search-result']"

            enlace = "//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']"
            precio = "//span[@data-a-color='base']/span[@class='a-offscreen']"
            precioAnterior = "//span[@data-a-color='secondary']/span[@class='a-price a-text-price']"
            califica = "//span[@class='a-declarative']/a/i/span[@class='a-icon-alt']"
            numCalifica = "//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style']/span[@class='a-size-base s-underline-text']"
            imagen = "//img[@class='s-image']"
            vendidosMesPasado = "//span[@class='a-size-base a-color-secondary']"

            try:
                pagina.wait_for_selector(contenidoPrincipal, timeout=10 * 1000)
            except PlaywrighTimeoutError:
                print(f"Error al cargar contenido. Vuelva a intentarlo en unos minutos.")

            pagina_actual = 1
            tmp = 0
            cont = 1
            while tmp < 8:
                tmp += 1
                print(f"Página de Scraping Nº {pagina_actual}")
                pagina.wait_for_timeout(timeout=tiempoAlea(8) * 1000)

                for content in pagina.query_selector_all(contenidoPrincipal):
                    link_relativo = catchClause.attributes(content.query_selector(enlace), 'href')
                    if link_relativo:
                        link_producto = "https://www.amazon.com" + link_relativo
                    else:
                        link_producto = "Sin enlace disponible"

                    datos = {
                        "Id":cont,
                        "Link Producto": link_producto,
                        "Producto": catchClause.text(content.query_selector(enlace)),
                        "ASIN": catchClause.attributes(content, 'data-asin'),
                        "Precio": catchClause.text(content.query_selector(precio)),
                        "Precio Original": catchClause.text(content.query_selector(precioAnterior)),
                        "Vendidos Mes Pasado": catchClause.text(content.query_selector(vendidosMesPasado)),
                        "Calificación": catchClause.text(content.query_selector(califica)),
                        "Num de Calificaciones": re.sub(r"\D", "", catchClause.text(content.query_selector(numCalifica))),
                        "Imagen": catchClause.attributes(content.query_selector(imagen), 'src'),
                    }
                    cont+=1

                    datosAmazon.append(datos)

                try:
                    siguiente = pagina.query_selector("//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']")
                    if siguiente:
                        siguiente.click()
                        pagina_actual += 1
                    else:
                        print("No se pudo encontrar el botón de siguiente. Terminando scraping.")
                        break
                except AttributeError:
                    print(f"Hay problemas con la sección {pagina.url}")
                    break

            navegador.close()
    except Exception as e:
        print(f"Ocurrió un error: {e}")

    print(f"Scraping realizado con éxito. Se guardará un archivo Excel")
    
    df = pd.DataFrame(datosAmazon)
    #df.to_excel(output_file, index=False)

    df.to_excel(f"./BasesDeDatos/{produbuscar}.xlsx", index=False)
 
    print(f"{produbuscar} se ha guardado con éxito")
    dfrecien = pd.read_excel(f"./BasesDeDatos/{produbuscar}.xlsx")
    print(dfrecien)