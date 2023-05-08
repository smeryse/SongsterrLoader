import json
from xml.etree.ElementTree import fromstring

import requests
from bs4 import BeautifulSoup


def get_soup(url: str) -> type(str):
    """
    Возвращает объект BeautifulSoup, созданный из HTML-кода страницы, полученной по URL-адресу.

    :param url:  URL-адрес страницы.
    :return bs4.BeautifulSoup: Объект BeautifulSoup, созданный из HTML-кода страницы.
    :raise requests.HTTPError: Если не удаётся получить страницу по URL-адресу.
    """

    # Отправка GET-запроса на сайт
    response = requests.get(url)
    response.raise_for_status()

    # Проверка успешности запроса
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        # Обработка ошибки
        print('Ошибка при запросе:', response.status_code)


def find_json_script(soup: type(BeautifulSoup)) -> type(str):
    """
   Выполняет поиск JSON-скрипта внутри предоставленного объекта BeautifulSoup.

   :param soup: A BeautifulSoup object.
   :return A string containing the JSON script.
    """
    json_script = soup.find('body').find('script', id='state')
    return str(json_script)[43:-9]


def get_revision_id(json_string: str) -> (str, str):
    """

    :param json_string: A JSON строка, содержащая следующие поля:
        'meta': {
            'current': {
                'revisionId': int,
                'title': str,
                'artist': str
            }
        }
    :return:Кортеж, содержащий извлеченный идентификатор ревизии в виде числа и название трека в виде строки.
    """
    # Распарсить JSON-строку в объект Python
    data = json.loads(json_string)['meta']['current']
    revision_id = data['revisionId']
    track_name = data['title'] + ' - ' + data['artist']
    return revision_id, track_name


def get_xml(revision_id: str) -> type(str):
    """
    Функция get_xml получает revision_id и возвращает attachment_url.

    :param revision_id: Идентификатор ревизии песни на сайте songsterr.com.
    :return: Ссылка на файл песни на сервере в формате GP5.
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


def download_gp5(download_url: str, file_name='file', path='media/gp5') -> [type(str), None]:
    """
    Функция для загрузки файлов формата gp5 на диск.

    :param download_url: URL-адрес файла для скачивания.
    :param file_name: Имя файла для сохранения, по умолчанию - 'file'.
    :param path: Путь для сохранения файла, по умолчанию - 'media'.
    :return:
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

        return f'{path}/{file_name}.gp5'
    else:
        # Обработка ошибки
        print('Ошибка при загрузке файла:', response.status_code)
        return None


def full_download_gp5(url: str) -> str:
    """
    Функция основного скрипта для загрузки файлов гитарных табулатур.

    :param url: (str): Ссылка на страницу с гитарными табулатурами.
    :return: File_path: Путь к скачанному файлу
    """
    soup = get_soup(url)
    json_string = find_json_script(soup)
    revision_id, track_name = get_revision_id(json_string)
    file_url = get_xml(revision_id)
    return download_gp5(file_url, file_name=track_name)


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
            return "https://www.songsterr.com" + str(first_song)
        else:
            return None
    except Exception as e:
        pass


# пример использования
if __name__ == '__main__':
    link = 'https://www.songsterr.com/a/wsa/joe-satriani-searching-tab-s39391'
    print(full_download_gp5(link))

# TODO Сделать обработку ошибка сервера код не 200. Чтобы пользователю нормально отправлялось
