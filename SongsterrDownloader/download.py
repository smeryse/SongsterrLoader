import json
from xml.etree.ElementTree import fromstring
from bs4 import BeautifulSoup
import requests


def get_html(url: str) -> type(str):
    """
    Возвращает объект BeautifulSoup, созданный из HTML-кода страницы, полученной по URL-адресу.

    Args:
        url (str): URL-адрес страницы.

    Returns:
        bs4.BeautifulSoup: Объект BeautifulSoup, созданный из HTML-кода страницы.

    Raises:
        requests.HTTPError: Если не удаётся получить страницу по URL-адресу.
    """
    response = requests.get(url)
    response.raise_for_status()

    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        # Обработка ошибки
        print('Ошибка при запросе:', response.status_code)


def find_json_script(soup: type(BeautifulSoup)) -> type(str):
    """
    Searches for a JSON script inside the provided BeautifulSoup object.

    Args:
    - soup: A BeautifulSoup object.

    Returns:
    - A string containing the JSON script.
    """
    json_script = soup.find('body').find('script', id='state')
    return str(json_script)[43:-9]


def get_revision_id(json_string: str) -> (str, str):
    """
    Args:
    json_string (str): A JSON string with at least the following fields:
        'meta': {
            'current': {
                'revisionId': int,
                'title': str,
                'artist': str
            }
        }

    Returns:
        tuple: A tuple containing the extracted revision ID as int and track name as str.
    """
    # Распарсить JSON-строку в объект Python
    data = json.loads(json_string)['meta']['current']
    revision_id = data['revisionId']
    track_name = data['title'] + ' - ' + data['artist']
    return revision_id, track_name


def get_xml(revision_id: str) -> type(str):
    """
    Функция get_xml получает revision_id и возвращает attachment_url.
    Args:
        revision_id (int): Идентификатор ревизии песни на сайте songsterr.com.

    Returns:
        str: Ссылка на файл песни в формате GP5.

    Raises:
        None
    """
    # создание ссылки
    url = f'https://www.songsterr.com/a/ra/player/songrevision/{revision_id}.xml'

    # Отправка GET-запроса на сайт
    response = requests.get(url)

    # Проверка успешности запроса
    if response.status_code == 200:
        # Получение текстового содержимого ответа (XML-кода)
        xml_string = response.text
        # Парсинг XML-кода
        root = fromstring(xml_string)

        # Получение значения attachmentUrl
        attachment_url = root.find('.//tab/guitarProTab/attachmentUrl').text
        return attachment_url
    else:
        # Обработка ошибки
        print('Ошибка при запросе:', response.status_code)


def download_gp5(download_url: str, file_name='file', path='files') -> [type(str), None]:
    """
    Функция для загрузки файлов формата gp5 на диск.
    Args:
        download_url (str): URL-адрес файла для скачивания.
        file_name (str, опционально): имя файла для сохранения, по умолчанию - 'file'.
        path (str, опционально): путь для сохранения файла, по умолчанию - 'files'.
    """
    # Отправка GET-запроса на сервер
    response = requests.get(download_url)

    # Проверка успешности запроса
    if response.status_code == 200:
        # Получение содержимого ответа (файла)
        file_content = response.content

        # Сохранение файла на диск
        with open(f'{path}/{file_name}.gp5', 'wb') as f:
            f.write(file_content)

        print('Файл загружен успешно.')
        return f'{path}/{file_name}.gp5'
    else:
        # Обработка ошибки
        print('Ошибка при загрузке файла:', response.status_code)
        return None


def main(url: str) -> None:
    """
    Функция основного скрипта для загрузки файлов гитарных табулатур.
    Args:
        url (str): Ссылка на страницу с гитарными табулатурами.
    Возвращает:
        None
    """
    soup = get_html(url)
    json_string = find_json_script(soup)
    revision_id, track_name = get_revision_id(json_string)
    file_url = get_xml(revision_id)
    download_gp5(file_url, file_name=track_name)

if __name__ == '__main__':
    with open('songs.txt', 'r') as songs:
        song_list = songs.readlines()
    print(song_list)
# TODO Сделать обработку ошибка сервера код не 200. Чтобы пользователю нормально отправлялось
