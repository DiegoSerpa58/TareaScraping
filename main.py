import requests
from bs4 import BeautifulSoup
import json


# URL objetivo (Hacker News)
url = "https://news.ycombinator.com/"

# Hacemos la petición HTTP y convertimos el HTML a texto.
# Luego lo parseamos con BeautifulSoup para poder buscar etiquetas fácilmente.
soup = BeautifulSoup(requests.get(url).text, "html.parser")

# Lista donde guardaremos el "dataset":
# cada elemento será un diccionario con title, points, time, comments.
noticias = []

# 2) EXTRACCIÓN DE DATOS POR BLOQUES (TR "athing" + subtext)

# (DOM):
# En Hacker News cada noticia está representada por 2 filas <tr> consecutivas:
#
#   - Fila 1: <tr class="athing">  -> contiene el título (y el id de la noticia)
#   - Fila 2: <tr> siguiente       -> contiene <td class="subtext"> con puntos, tiempo y comentarios
#
# Por eso, para cada fila "athing" (fila del título), "saltamos" a la fila hermana
# inmediatamente siguiente usando find_next_sibling("tr") para obtener el subtext.

# Iterar sobre cada noticia (fila con clase "athing")
for fila in soup.find_all("tr", class_="athing"):

    #  EXTRAER EL TÍTULO
    # Dentro de la fila "athing", el título suele estar en:
    # <span class="titleline"><a>...</a></span>
    #
    # .a toma el primer <a> dentro del span.
    titulo = fila.find("span", class_="titleline").a.get_text(strip=True)

    # SALTAR A LA FILA HERMANA (subtext row)
    # El subtext está en la siguiente fila (tr) después de la fila de la noticia.
    # find_next_sibling("tr") = "dame el <tr> inmediatamente debajo de este <tr>"
    # Luego buscamos el td.subtext donde están puntos, tiempo y comentarios.
    subtext = fila.find_next_sibling("tr").find("td", class_="subtext")

    puntos = int(subtext.find("span", class_="score").text.split()[0]) if subtext.find("span", class_="score") else 0

    # El tiempo relativo suele estar en: <span class="age">5 hours ago</span>
    # Si no existe, ponemos "N/A" para mantener consistencia del dataset.
    tiempo = subtext.find("span", class_="age").text if subtext.find("span", class_="age") else "N/A"

    #EXTRAER NÚMERO DE COMENTARIOS
   
    # En el bloque subtext hay varios enlaces <a>.
    # El último enlace normalmente es:
    # - "158 comments" / "1 comment"  -> tomamos el número
    # - "discuss"                     -> significa 0 comentarios
    # Inicializamos comentarios en 0 por defecto.
    comentarios = 0

    # Recorremos los enlaces al revés (reversed) para encontrar primero el enlace final
    for link in reversed(subtext.find_all("a")):
        txt = link.text  # texto del enlace

        # Si el texto contiene la palabra "comment", extraemos el número
        # Ej: "158 comments" -> txt.split()[0] -> "158" -> int(...) -> 158
        if "comment" in txt:
            comentarios = int(txt.split()[0])
            break

        # Si dice "discuss", se queda en 0 y terminamos
        elif txt == "discuss":
            break

    # GUARDAR LA NOTICIA EN EL DATASET
    # Creamos un diccionario por noticia (unidad de información completa)
    # y lo agregamos a la lista noticias.
    noticias.append({
        "title": titulo,
        "points": puntos,
        "time": tiempo,
        "comments": comentarios
    })



#MOSTRAR TABLA GENERAL EN CONSOLA

print(f"Total de noticias extraídas: {len(noticias)}")
print("="*120)
print(f"{'#':<4} {'TÍTULO':<50} {'POINTS':<10} {'TIME':<20} {'COMMENTS':<10}")
print("="*120)

# recorremos (iteramos) el dataset
# en el orden en que aparecieron en la página.
for i, n in enumerate(noticias, 1):
    # Truncamos el título para que no rompa el formato de la tabla
    titulo = n['title'][:47] + "..." if len(n['title']) > 50 else n['title']

    # Imprimimos cada fila de la tabla con sus columnas
    print(f"{i:<4} {titulo:<50} {n['points']:<10} {n['time']:<20} {n['comments']:<10}")

# LISTA DE DICCIONARIOS
# Mostramos las primeras 5 noticias en formato JSON para visualizar la estructura
# del dataset (lista de diccionarios).

print("\n" + "="*120)
print(f"{'LISTA DE DICCIONARIOS (Primeras 5 noticias)':^120}")

print(json.dumps(noticias[:5], indent=2, ensure_ascii=False))

# Filtrar las noticias que tengan más de 100 puntos.
# Ordenarlas de mayor a menor popularidad (puntos).

print("\n" + "="*120)
print(f"{'NOTICIAS POPULARES (>100 POINTS)':^120}")

#Filtrado:

# crear una nueva lista solo con noticias cuyo points sea > 100"
# Ordenamiento:
# significa: "ordenar por el campo points, de mayor a menor"
noticias_populares = sorted(
    [n for n in noticias if n["points"] > 100],
    key=lambda x: x["points"],
    reverse=True
)

print(f"Total de noticias con más de 100 puntos: {len(noticias_populares)}")
print("="*120)
# Truncar título si es muy largo para mantener formato de tabla
print(f"{'#':<4} {'TÍTULO':<50} {'POINTS':<10} {'TIME':<20} {'COMMENTS':<10}")
print("="*120)

# Imprimir noticias populares (ya filtradas y ordenadas)
for i, n in enumerate(noticias_populares, 1):
    # Truncar título si es muy largo para mantener formato de tabla
    titulo = n['title'][:47] + "..." if len(n['title']) > 50 else n['title']
    print(f"{i:<4} {titulo:<50} {n['points']:<10} {n['time']:<20} {n['comments']:<10}")

print("="*120)

# 6) LISTA FINAL (POPULARES EN FORMATO JSON)
# Aquí imprimimos la lista COMPLETA de populares como lista de diccionarios.

print(f"{'NOTICIAS POPULARES - FORMATO LISTA DE DICCIONARIOS':^120}")
print("="*120 + "\n")

print(json.dumps(noticias_populares, indent=2, ensure_ascii=False))

print("\n" + "="*120)
print(f"\n Extracción completada exitosamente")
print(f" Dataset completo: {len(noticias)} noticias")
print(f" Noticias populares (>100 points): {len(noticias_populares)} noticias")
print(f" Ordenadas de mayor a menor popularidad\n")
