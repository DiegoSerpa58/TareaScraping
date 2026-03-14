import requests
from bs4 import BeautifulSoup

# URL de Hacker News
url = "https://news.ycombinator.com/"

# Realizar la petición HTTP
response = requests.get(url)

# Crear el objeto BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Lista para almacenar todas las noticias
noticias = []

# Iterar sobre cada fila con clase "athing" (contiene el título)
for fila_titulo in soup.find_all("tr", class_="athing"):
    
    # Extraer el título
    span_titleline = fila_titulo.find("span", class_="titleline")
    if not span_titleline:
        continue
    
    a_tag = span_titleline.find("a")
    if not a_tag:
        continue
    
    titulo = a_tag.get_text(strip=True)
    
    # Buscar la fila hermana siguiente que contiene subtext (puntos, tiempo, comentarios)
    fila_subtext = fila_titulo.find_next_sibling("tr")
    
    # Inicializar valores por defecto
    puntos = 0
    tiempo = "N/A"
    comentarios = 0
    
    # Si existe la fila subtext, extraer la información
    if fila_subtext:
        subtext = fila_subtext.find("td", class_="subtext")
        
        if subtext:
            # Extraer PUNTOS
            score_span = subtext.find("span", class_="score")
            if score_span:
                # El texto es algo como "1535 points"
                texto_puntos = score_span.get_text(strip=True)
                puntos = int(texto_puntos.split()[0])  # Tomar solo el número
            
            # Extraer TIEMPO
            age_span = subtext.find("span", class_="age")
            if age_span:
                a_time = age_span.find("a")
                if a_time:
                    tiempo = a_time.get_text(strip=True)
            
            # Extraer COMENTARIOS
            # Los comentarios están en el último <a> que contiene la palabra "comment"
            links = subtext.find_all("a")
            for link in reversed(links):  # Revisar desde el último hacia atrás
                texto_link = link.get_text(strip=True)
                if "comment" in texto_link:
                    # Puede ser "158 comments" o "1 comment"
                    comentarios = int(texto_link.split()[0])
                    break
                elif texto_link == "discuss":
                    # Si dice "discuss", no hay comentarios aún
                    comentarios = 0
                    break
    
    # Crear el diccionario de la noticia
    noticia = {
        "title": titulo,
        "points": puntos,
        "time": tiempo,
        "comments": comentarios
    }
    
    # Agregar a la lista
    noticias.append(noticia)

# Mostrar los resultados en formato de tabla

print(f"Total de noticias extraídas: {len(noticias)}")
print("="*120)
print(f"{'#':<4} {'TÍTULO':<50} {'POINTS':<10} {'TIME':<20} {'COMMENTS':<10}")
print("="*120)

for i, noticia in enumerate(noticias, 1):
    # Truncar título si es muy largo
    titulo_corto = noticia['title'][:47] + "..." if len(noticia['title']) > 50 else noticia['title']
    
    print(f"{i:<4} {titulo_corto:<50} {noticia['points']:<10} {noticia['time']:<20} {noticia['comments']:<10}")



# Mostrar también como lista de diccionarios
print("\n" + "="*120)
print(f"{'LISTA DE DICCIONARIOS (Primeras 5 noticias)':^120}")
print("="*120 + "\n")

import json
print(json.dumps(noticias[:5], indent=2, ensure_ascii=False))


# FASE 4: DESAFÍO DE CLASIFICACIÓN (BONUS)
print("\n" + "="*120)
print(f"{'NOTICIAS POPULARES (>100 POINTS)':^120}")


# Filtrar noticias con más de 100 puntos
noticias_populares = [noticia for noticia in noticias if noticia['points'] > 100]

# Ordenar de mayor a menor popularidad (por puntos)
noticias_populares_ordenadas = sorted(noticias_populares, key=lambda x: x['points'], reverse=True)

print(f"Total de noticias con más de 100 puntos: {len(noticias_populares_ordenadas)}")
print("="*120)
print(f"{'#':<4} {'TÍTULO':<50} {'POINTS':<10} {'TIME':<20} {'COMMENTS':<10}")
print("="*120)

for i, noticia in enumerate(noticias_populares_ordenadas, 1):
    # Truncar título si es muy largo
    titulo_corto = noticia['title'][:47] + "..." if len(noticia['title']) > 50 else noticia['title']
    
    print(f"{i:<4} {titulo_corto:<50} {noticia['points']:<10} {noticia['time']:<20} {noticia['comments']:<10}")


# Mostrar también en formato de lista de diccionarios
print("\n" + "="*120)
print(f"{'NOTICIAS POPULARES - FORMATO LISTA DE DICCIONARIOS':^120}")
print("="*120 + "\n")

print(json.dumps(noticias_populares_ordenadas, indent=2, ensure_ascii=False))

print("\n" + "="*120)
print(f"\n Extracción completada exitosamente")
print(f" Dataset completo: {len(noticias)} noticias")
print(f" Noticias populares (>100 points): {len(noticias_populares_ordenadas)} noticias")
print(f" Ordenadas de mayor a menor popularidad\n") 