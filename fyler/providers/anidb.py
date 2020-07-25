import csv
from pathlib import Path
import logging
import zlib
from datetime import date

import requests
import textdistance
from ratelimit import limits, sleep_and_retry
from diskcache import Cache
import bs4
from bs4 import BeautifulSoup
import heapq

from appdirs import AppDirs

from .provider import Provider
from fyler.models import Media, Series, Episode, Movie

dirs = AppDirs('fyler', 'fyler')
_cache_dir = Path(dirs.user_cache_dir) / 'anidb'
_titles_dat = Path(dirs.user_cache_dir) / 'anidb/data/anime-titles.dat'
_cache_dir.mkdir(parents=True, exist_ok=True)
cache = Cache(directory=str(_cache_dir))

logger = logging.getLogger(__name__)


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
    logger.debug('Requesting from AniDB')
    return _rl_get('http://api.anidb.net:9001/httpapi', params=args).text


class AniDBProvider(Provider):
    name = 'AniDB'

    def detail(self, media):
        return self.get_info(media.id)

    def get_info(self, id: int) -> Media:
        xml = _raw_get_info(id)
        soup = BeautifulSoup(xml, 'xml')
        anime = soup.find('anime')

        anime_kwargs = {
            'database': 'AniDB',
            'id': id,
            'date': date.fromisoformat(anime.find('startdate').text),
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
                    'series': None,  # Will be set later
                    'id': int(episode.attrs['id']),
                    'date': date.fromisoformat(episode.find('airdate').text),
                    'season_number': None,
                    'episode_number': int(episode.find('epno').text),  # I want this to be an int, but sometimes its different (specials?)
                }
                for title in episode.find_all('title'):
                    if title.attrs['xml:lang'] == 'en':
                        episode_kwargs['title'] = title.text
                        break
                episodes.append(Episode(**episode_kwargs))
            episodes.sort(key=lambda x: x.episode_number)
            anime_kwargs['episodes'] = episodes

            s = Series(**anime_kwargs)
            for e in s.episodes:
                e.series = s
            return s
        elif anime.find('type').text == 'Movie':
            return Movie(**anime_kwargs)
        else:
            raise ValueError('Anime is not a TV Series or Movie')

    def download_title_data(self):
        _titles_dat.parent.mkdir(parents=True, exist_ok=True)
        with open(_titles_dat, 'wb') as dat:
            with requests.get(
                'https://anidb.net/api/anime-titles.dat.gz',
                headers={'User-Agent': 'fyler'},
                stream=True
            ) as response:
                response.raise_for_status()
                z = zlib.decompressobj(wbits=zlib.MAX_WBITS | 16)  # Detect gzip automatically
                for chunk in response.iter_content(chunk_size=8192):
                    dat.write(z.decompress(chunk))
                dat.write(z.flush())

    def _search_by_name(self, query: str) -> list:
        """
        Searches for the closest match to query. Note that this function
        loads the dat file every time, and is not recommended for multiple searches.
        """
        if not _titles_dat.exists():
            logger.info('AniDB title data not found. Downloading fresh copy...')
            self.download_title_data()

        key = lambda x: textdistance.levenshtein.normalized_similarity(query, x[3])
        with open(_titles_dat, newline='') as f:
            # Filter by primary title
            reader = csv.reader(f, delimiter='|')
            for _ in range(3):
                next(reader)  # Header
            reader = filter(lambda k: int(k[1]) == 1, reader)
            return heapq.nlargest(10, reader, key=key)

    def search(self, query: str) -> list:
        return [
            Media(
                database=self.name,
                title=k[3],
                id=int(k[0]),
                date=None,
            )
            for k in self._search_by_name(query)
        ]
