import csv
from pathlib import Path
import logging

import requests
import textdistance
from ratelimit import limits, sleep_and_retry
from diskcache import Cache
import bs4
from bs4 import BeautifulSoup

from . import provider

_titles_dat = Path(__file__).parent / 'data/anime-titles.dat'
_cache_dir = Path.home() / '.cache/fyler'

_cache_dir.mkdir(parents=True, exist_ok=True)
cache = Cache(directory=str(_cache_dir))

logging.basicConfig(level=logging.DEBUG)


@sleep_and_retry
@limits(calls=2, period=5)
def _rl_get(*args, **kwargs):
    return requests.get(*args, **kwargs)


@cache.memoize(expire=60 * 60 * 24 * 30)  # Cache for 1 month
def _raw_get_info(id: int) -> str:
    args = {
        'request': 'anime',
        'client': 'fyler',
        'clientver': '1',
        'protover': '1',
        'aid': str(id),
    }
    print('Requesting from AniDB')
    return _rl_get('http://api.anidb.net:9001/httpapi', params=args).text


class AniDBProvider(provider.Provider):
    def __init__(self):
        pass

    def get_info(self, id: int) -> provider.Media:
        xml = _raw_get_info(id)
        soup = BeautifulSoup(xml, 'xml')
        anime = soup.find('anime')

        anime_kwargs = {
            'database': 'AniDB',
            'id': id,
            'overview': anime.find('description').text,
            'rating': float(anime.find('ratings').find('permanent').text),
        }
        for title in anime.find('titles').find_all('title'):
            if title.attrs['type'] == 'main':
                anime_kwargs['title'] = title.text
                break

        if anime.find('type').text == 'TV Series':
            episodes = []
            for episode in anime.find('episodes').children:
                if not isinstance(episode, bs4.element.Tag):
                    continue
                if episode.find('epno').attrs['type'] != '1':
                    continue
                episode_kwargs = {
                    'database': 'AniDB',
                    'series_id': id,
                    'id': int(episode.attrs['id']),
                    'season_number': None,
                    'episode_number': int(episode.find('epno').text),  # I want this to be an int, but sometimes its different (specials?)
                    'overview': episode.find('summary').text,
                    'rating': float(episode.find('rating').text),
                }
                for title in episode.find_all('title'):
                    if title.attrs['xml:lang'] == 'en':
                        episode_kwargs['title'] = title.text
                        break
                episodes.append(provider.Episode(**episode_kwargs))
            episodes.sort(key=lambda x: x.episode_number)
            anime_kwargs['episodes'] = episodes

            return provider.Series(**anime_kwargs)
        elif anime.find('type').text == 'Movie':
            return provider.Movie(**anime_kwargs)
        else:
            raise ValueError('Anime is not a TV Series or Movie')

    def _search_for_id(self, query: str) -> int:
        """
        Searches for the closest match to query. Note that this function
        loads the dat file every time, and is not recommended for multiple searches.
        """
        key = lambda x: textdistance.levenshtein.normalized_similarity(query, x[3])
        with open(_titles_dat, newline='') as f:
            reader = csv.reader(f, delimiter='|')
            for _ in range(3):
                next(reader)  # Header
            return int(max(reader, key=key)[0])

    def search(self, query: str) -> provider.Media:
        return self.get_info(self._search_for_id(query))
