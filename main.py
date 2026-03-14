import requests
from bs4 import BeautifulSoup
import json

URL = "https://news.ycombinator.com/"


def extraer_noticias(url: str) -> list[dict]:
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    noticias = []

    for athing in soup.select("tr.athing"):
        # Title
        a = athing.select_one("span.titleline a")
        if not a:
            continue
        title = a.get_text(strip=True)

        # Subtext row (sibling)
        sub = athing.find_next_sibling("tr")
        subtext = sub.select_one("td.subtext") if sub else None

        # Defaults for missing data
        points = 0
        time = "N/A"
        comments = 0

        if subtext:
            score = subtext.select_one("span.score")
            if score:
                # "153 points" -> 153
                points = int(score.get_text(strip=True).split()[0])

            age = subtext.select_one("span.age a")
            if age:
                time = age.get_text(strip=True)

            # Comments: last <a> often is comments or "discuss"
            last_a = subtext.select("a")[-1] if subtext.select("a") else None
            if last_a:
                txt = last_a.get_text(strip=True).lower()
                if "comment" in txt:
                    comments = int(txt.split()[0])  # "158 comments" -> 158
                elif txt == "discuss":
                    comments = 0

        noticias.append({"title": title, "points": points, "time": time, "comments": comments})

    return noticias


def imprimir_tabla(data: list[dict], titulo: str) -> None:
    # Column widths (simple & readable)
    w_num, w_title, w_points, w_time, w_comments = 4, 60, 8, 20, 10

    def cut(s: str, w: int) -> str:
        return (s[: w - 3] + "...") if len(s) > w else s

    print("\n" + "=" * 120)
    print(f"{titulo:^120}")
    print("=" * 120)
    print(f"{'#':<{w_num}} {'TÍTULO':<{w_title}} {'PTS':<{w_points}} {'TIME':<{w_time}} {'COMMENTS':<{w_comments}}")
    print("-" * 120)

    for i, n in enumerate(data, 1):
        print(
            f"{i:<{w_num}} "
            f"{cut(n['title'], w_title):<{w_title}} "
            f"{n['points']:<{w_points}} "
            f"{cut(n['time'], w_time):<{w_time}} "
            f"{n['comments']:<{w_comments}}"
        )

    print("=" * 120)
    print(f"Total: {len(data)}")


if __name__ == "__main__":
    noticias = extraer_noticias(URL)

    # Fase 3: Dataset completo (tabla)
    imprimir_tabla(noticias, "DATASET")

    # Lista de diccionarios (si la necesitas para entregar / verificar)
    print("\nLISTA DE DICCIONARIOS (primeras 5):")
    print(json.dumps(noticias[:5], indent=2, ensure_ascii=False))

    # Fase 4 (Bonus): Filtrar > 100 puntos y ordenar desc por points
    populares = sorted([n for n in noticias if n["points"] > 100], key=lambda x: x["points"], reverse=True)
    imprimir_tabla(populares, "POPULARES (> 100 PUNTOS)")