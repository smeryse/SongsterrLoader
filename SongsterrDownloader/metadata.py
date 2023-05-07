import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from config import SPOTIFY_CLIENT_SECRET, SPOTIFY_CLIENT_ID


def search_track(query):
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

    # Возвращаем метаданные трека
    return {
        'id': track['id'],
        'name': track['name'],
        'artists': [artist['name'] for artist in track['artists']],
        'album': track['album']['name'],
        'album_id': track['album']['id'],
        'preview_url': track['preview_url'],
        'duration_ms': track['duration_ms']
    }


if __name__ == '__main__':
    track = search_track('Radiohead - Creep')
    print(track)
