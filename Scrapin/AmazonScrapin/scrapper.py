import time
from tools import scraping
from limpieza_datos_amz import Clean
import amazon_cat

tiempoInicio = time.time()

full_categories = amazon_cat.main()
make_headless = True
categories = [cat['nombre'] for cat in full_categories]
print(f"Buscare las siguientes categorias {categories}")
for cat in categories:
    scraping(make_headless, cat)

tiempoTotal = round(time.time()-tiempoInicio,2)
tiempoSegundos = round(tiempoTotal)
tiempoMinutos = round(tiempoTotal/60)

print(f"Tiempo requerido: {tiempoMinutos} o {tiempoSegundos} segundos")

Clean()