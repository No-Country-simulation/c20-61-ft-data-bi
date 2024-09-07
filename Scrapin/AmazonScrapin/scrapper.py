import time
from tools import scraping
from limpieza_datos_amz import Clean

tiempoInicio = time.time()

make_headless = True
#Categorias = ["Zapatos","Almohadas","Tecnologia"]
Categorias = ["Repelente"]
for cat in Categorias:
    scraping(make_headless, cat)

tiempoTotal = round(time.time()-tiempoInicio,2)
tiempoSegundos = round(tiempoTotal)
tiempoMinutos = round(tiempoTotal/60)

print(f"Tiempo requerido: {tiempoMinutos} o {tiempoSegundos} segundos")

Clean()