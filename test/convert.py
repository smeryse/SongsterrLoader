import requests
from bs4 import BeautifulSoup

url = f"https://www.songsterr.com/a/wa/search?pattern=home"

# отправляем запрос и получаем HTML-страницу с результатами поиска
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

result = soup.find("div", {"class": "Ccm1w1 Ccm1n1", "data-list": "songs"})

print(result.text)
