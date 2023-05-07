import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

from SongsterrDownloader.find import search_songsterr

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home_page.html')


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    link = f"https://www.songsterr.com/a/wa/search?pattern={query}"
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    div_list = soup.find('div', {'data-list': 'songs', 'class': "Ccm1w1 Ccm1n1"})
    # создаем пустой список для хранения данных
    tracks = []
    print(div_list)
    # проходим по каждому тегу <div> в списке и извлекаем нужные данные
    for song in div_list.find_all('a', {'data-song': True}):
        title = song.div.find('div', {'class':'B0c2e8'}).text
        artist = song.div.find('div', {'class':'B0c21e'}).text
        link = 'https://www.songsterr.com' + song['href']
        hard_lvl = song.span['title']
        tracks.append({'title': title, 'artist': artist,
                       'link': link, 'hard_lvl': hard_lvl})

    # передаем список треков в шаблон Jinja2
    return render_template('result.html', tracks=tracks)


if __name__ == '__main__':
    app.run(debug=True)
