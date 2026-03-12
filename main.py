import requests
from bs4 import BeautifulSoup

url = "https://news.ycombinator.com/"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

titulos = []
for span in soup.find_all("span", class_="titleline"):
    a = span.find("a")
    if not a:
        continue
    titulo = a.get_text(strip=True)
    titulos.append(titulo)

# print(titulos)

for i in titulos:
    print(i)