import requests
from bs4 import BeautifulSoup
import json

url = "https://news.ycombinator.com/"
soup = BeautifulSoup(requests.get(url).text, "html.parser")

noticias = []

for fila in soup.find_all("tr", class_="athing"):

    titulo = fila.find("span", class_="titleline").a.get_text(strip=True)
    subtext = fila.find_next_sibling("tr").find("td", class_="subtext")

    puntos = int(subtext.find("span", class_="score").text.split()[0]) if subtext.find("span", class_="score") else 0
    tiempo = subtext.find("span", class_="age").text if subtext.find("span", class_="age") else "N/A"

    comentarios = 0
    for link in reversed(subtext.find_all("a")):
        txt = link.text
        if "comment" in txt:
            comentarios = int(txt.split()[0])
            break
        elif txt == "discuss":
            break

    noticias.append({
        "title": titulo,
        "points": puntos,
        "time": tiempo,
        "comments": comentarios
    })

# TABLA GENERAL
print(f"Total de noticias extraídas: {len(noticias)}")
print("="*120)
print(f"{'#':<4} {'TÍTULO':<50} {'POINTS':<10} {'TIME':<20} {'COMMENTS':<10}")
print("="*120)

for i, n in enumerate(noticias, 1):
    titulo = n['title'][:47] + "..." if len(n['title']) > 50 else n['title']
    print(f"{i:<4} {titulo:<50} {n['points']:<10} {n['time']:<20} {n['comments']:<10}")

print("="*120)

# LISTA DE DICCIONARIOS
print("\n" + "="*120)
print(f"{'LISTA DE DICCIONARIOS (Primeras 5 noticias)':^120}")
print("="*120 + "\n")

print(json.dumps(noticias[:5], indent=2, ensure_ascii=False))

print("\n" + "="*120)

# FASE 4: CLASIFICACIÓN
print("\n" + "="*120)
print(f"{'FASE 4: DESAFÍO DE CLASIFICACIÓN - NOTICIAS POPULARES (>100 POINTS)':^120}")
print("="*120)

noticias_populares = sorted(
    [n for n in noticias if n["points"] > 100],
    key=lambda x: x["points"],
    reverse=True
)

print(f"Total de noticias con más de 100 puntos: {len(noticias_populares)}")
print("="*120)
print(f"{'#':<4} {'TÍTULO':<50} {'POINTS':<10} {'TIME':<20} {'COMMENTS':<10}")
print("="*120)

for i, n in enumerate(noticias_populares, 1):
    titulo = n['title'][:47] + "..." if len(n['title']) > 50 else n['title']
    print(f"{i:<4} {titulo:<50} {n['points']:<10} {n['time']:<20} {n['comments']:<10}")

print("="*120)

# LISTA FINAL
print("\n" + "="*120)
print(f"{'NOTICIAS POPULARES - FORMATO LISTA DE DICCIONARIOS':^120}")
print("="*120 + "\n")

print(json.dumps(noticias_populares, indent=2, ensure_ascii=False))

print("\n" + "="*120)
print(f"\n✓ Extracción completada exitosamente")
print(f"✓ Dataset completo: {len(noticias)} noticias")
print(f"✓ Noticias populares (>100 points): {len(noticias_populares)} noticias")
print(f"✓ Ordenadas de mayor a menor popularidad\n")