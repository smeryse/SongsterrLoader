import os
from urllib.parse import urlencode
from urllib.request import urlopen

from pytube import YouTube


def search_video_on_youtube(query: str) -> str:
    """Поиск видео на YouTube и возвращение ссылки на первый результат.
    :arg query - поисковой запрос
    :return video.watch_url - ссылка на видео YouTube
    """

    # Кодирование запроса для передачи в URL.
    query = urlencode({'search_query': query})

    # Формирование URL для поиска на YouTube.
    link = 'https://www.youtube.com/results?' + query

    # Отправка запроса на страницу поиска и получение HTML-кода.
    html = urlopen(link).read()

    # Извлечение из HTML-кода идентификатора первого видео.
    start = html.decode().find('/watch?v=')
    end = html.decode().find('"', start)
    video_id = html.decode()[start + 9:end]

    # Получение ссылки на видео с помощью библиотеки pytube.
    link = 'https://www.youtube.com/watch?v=' + video_id
    video = YouTube(link)
    return video.watch_url


def download_audio_youtube(url_or_id: str, output_path='../media/music') -> str:
    """
    Функция загружает аудио с YouTube видео, используя модуль Pytube.

    :param output_path: Путь для сохранения файла.
    :arg url_or_id (str) - URL или идентификатор видео YouTube для загрузки аудио.
    :return str - Путь к загруженному аудио файлу.
    """
    yt = YouTube(url_or_id)
    audio = yt.streams.filter(only_audio=True).first()
    audio_title = yt.title

    # скачиваем трек в папку music
    audio.download(output_path=output_path, filename=f'{audio_title}.mp3')
    file_path = f"{output_path}/{audio_title}.mp3"

    # переименовываем файл в аудио формат
    # os.rename(f"../media/{audio_title}.mp4", file_path)
    return file_path


if __name__ == '__main__':
    # пример использования
    name = 'black hole sun'
    link = search_video_on_youtube(name)
    path = download_audio_youtube(link)
    print(path)
