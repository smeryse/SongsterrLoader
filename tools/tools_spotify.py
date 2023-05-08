import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from start.config import SPOTIFY_CLIENT_SECRET, SPOTIFY_CLIENT_ID


class Track:
    def __init__(self, id, name, artists, album, album_id, preview_url, duration_ms, cover_url, spotify_url):
        self.id = id
        self.name = name
        self.artists = artists
        self.album = album
        self.album_id = album_id
        self.preview_url = preview_url
        self.duration_ms = duration_ms
        self.cover_url = cover_url
        self.spotify_url = spotify_url


def search_track_on_spotify(query):
    """
    Ищет трек на Spotify по запросу и возвращает метаданные найденного трека.

    :arg query - Запрос для поиска трека на Spotify.

    :return dict: Словарь с метаданными найденного трека, включая идентификатор, название, исполнителей,
              название альбома, идентификатор альбома, ссылку на аудио-превью, продолжительность,
              ссылку на обложку и ссылку на трек на Spotify.
              Возвращает None, если трек не найден.
    """

    # Аутентифицируйтесь с помощью учетных данных клиента
    client_credentials_manager = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Ищем треки по запросу и получаем первый найденный трек
    results = sp.search(q=query, type='track', limit=1)
    if len(results['tracks']['items']) == 0:
        print('Трек не найден')
        return None
    track = results['tracks']['items'][0]
    # Возвращаем метаданные трека, включая обложку и ссылку на трек на Spotify
    return Track(
        track['id'],
        track['name'],
        [artist['name'] for artist in track['artists']],
        track['album']['name'],
        track['album']['id'],
        track['preview_url'],
        track['duration_ms'],
        track['album']['images'][0]['url'],
        track['external_urls']['spotify']
    )


if __name__ == '__main__':
    print(search_track_on_spotify('stay alone').album)
