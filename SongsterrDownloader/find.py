import requests
from bs4 import BeautifulSoup


def search_songsterr(query):
    try:
        # формируем URL-адрес для запроса
        url = f"https://www.songsterr.com/a/wa/search?pattern={query}"

        # отправляем запрос и получаем HTML-страницу с результатами поиска
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # извлекаем первый результат из списка
        result = soup.find("div", {"class": "Ccm1w1 Ccm1n1", "data-list": "songs"})
        first_song = result.find("a", {"class": "B0cew"})["href"]
        # проверяем, что результат найден
        if first_song:
            # извлекаем ссылку на страницу с табулатурой
            link = "https://www.songsterr.com" + str(first_song)
            return link
        else:
            return None
    except:
        pass


# пример использования
if __name__ == '__main__':
    song_list = '''
    Thrash Metal Cassette
    Back Foot
    Stupid Heavy Metal Broken Hearted Loser Punk
    Celebrity Mansions
    Round The Bend
    Pouring Gasoline
    Black Limousine
    K West
    Professional Freak
    Long Way Down'''.split('\n')

    for song_title in song_list:
        link = search_songsterr(song_title)
        if link:
            print(f"'{song_title}': {link}")
        else:
            print(f"Табулатура для '{song_title}' не найдена")


