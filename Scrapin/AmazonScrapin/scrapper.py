import time
from tools import scraping
from limpieza_datos_amz import Clean
import amazon_cat

tiempoInicio = time.time()

full_categories = amazon_cat.main()
make_headless = True
categories = [cat['nombre'] for cat in full_categories]
categories = ["Arte y artesanías","Automotriz","Bebé","Belleza y cuidado personal","Cine y TV","Computadoras","Deportes y actividades al aire libre",
              "Electrónicos","Equipaje","Herramientas y mejoramiento del hogar","Hogar y cocina","Industrial y cientifico","Insumo para mascotas",
              "Juguetes y juegos","Libros","Moda de niñas","Moda de niños","Moda para hombre","Moda para mujer","Musca MP3","Musica, CD y vinilos",
              "Salud y productos para el hogar","Software","Tienda kindle","Todos los departamentos","Videojuegos"]
print(f"Buscare las siguientes categorias {categories}")
for cat in categories:
    scraping(make_headless, cat)

tiempoTotal = round(time.time()-tiempoInicio,2)
tiempoSegundos = round(tiempoTotal)
tiempoMinutos = round(tiempoTotal/60)

print(f"Tiempo requerido: {tiempoMinutos} o {tiempoSegundos} segundos")

Clean()