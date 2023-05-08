import requests
from bs4 import BeautifulSoup
from flask import Flask, send_file, render_template, request

from tools.tools_songsterr import full_download_gp5
from tools.tools_spotify import search_track_on_spotify
from tools.tools_youtube import download_audio_youtube
from tools.tools_youtube import search_video_on_youtube

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('main_page.html')


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    link = f"https://www.songsterr.com/a/wa/search?pattern={query}"
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    div_list = soup.find('div', {'data-list': 'songs', 'class': "Ccm1w1 Ccm1n1"})
    # создаем пустой список для хранения данных
    tracks = []
    # проходим по каждому тегу <div> в списке и извлекаем нужные данные
    for song in div_list.find_all('a', {'data-song': True}):
        title = song.div.find('div', {'class': 'B0c2e8'}).text
        artist = song.div.find('div', {'class': 'B0c21e'}).text
        link = 'https://www.songsterr.com' + song['href']
        hard_lvl = song.span['title']
        tracks.append({'title': title, 'artist': artist,
                       'link': link, 'hard_lvl': hard_lvl})
        # сделать отображение уровня сложности рядом с треком

    # передаем список треков в шаблон Jinja2
    return render_template('search_result.html', tracks=tracks)


@app.route('/track_page', methods=['GET'])
def track_page():
    # получаем ссылку от пользователя
    link = request.args.get('link')

    # парсим сайт по ссылке
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')

    # получаем название и автора трека
    header = soup.find('h1', {'class': 'C612su'})
    title = header.find('span', {'aria-label': 'title'}).text
    artist = header.find('a', {'aria-label': 'artist'}).text

    # ищем метаданные трека на spotify
    query = f'{title} - {artist}'
    metadata = search_track_on_spotify(query)
    metadata.songsterr_link = link
    metadata.youtube_link = search_video_on_youtube(query)

    # передаем список треков в шаблон Jinja2
    return render_template('track_page.html',
                           track=metadata)


@app.route('/download_track', methods=['GET'])
def download_track():
    youtube_link = request.args.get('youtube_link')
    print(youtube_link)
    file_path = download_audio_youtube(youtube_link)
    print(file_path)
    return send_file(file_path, as_attachment=True)


@app.route('/download_score', methods=['GET'])
def download_score():
    songsterr_link = request.args.get('songsterr_link')
    file_path = full_download_gp5(songsterr_link)
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
