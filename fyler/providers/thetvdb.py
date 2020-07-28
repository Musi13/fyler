import logging
from datetime import date
from pathlib import Path

import requests
from appdirs import AppDirs
from diskcache import Cache

from fyler.models import Media, Series, Episode
from .provider import Provider

# Redefine dirs since importing settings causes a circular import
dirs = AppDirs('fyler', 'fyler')
_cache_dir = Path(dirs.user_cache_dir) / 'thetvdb'
_cache_dir.mkdir(parents=True, exist_ok=True)
cache = Cache(directory=str(_cache_dir))

API_ROOT = 'https://api.thetvdb.com'
API_KEY = '2212209a47d8300a7b5c292b8619c7a3'

logger = logging.getLogger(__name__)


@cache.memoize(expire=60 * 60 * 24)  # Tokens are valid for 24 hours
def _get_jwt_token() -> str:
    response = requests.post(f'{API_ROOT}/login', json={'apikey': API_KEY})
    response.raise_for_status()
    return response.json()['token']


class TheTVDBProvider(Provider):
    name = 'TheTVDB'

    def detail(self, media: Media) -> Media:
        response = requests.get(
            f'{API_ROOT}/series/{media.id}',
            headers={'Authorization': f'Bearer {_get_jwt_token()}'}
        )
        response.raise_for_status()
        parsed = response.json()['data']
        series = Series(
            database=self.name,
            id=media.id,
            date=date.fromisoformat(parsed['firstAired']),  # TODO
            title=parsed['seriesName'],
            episodes=None
        )

        last = 0
        page = 1
        episodes = []
        while not last:
            response = requests.get(
                f'{API_ROOT}/series/{media.id}/episodes',
                params={'page': page},
                headers={'Authorization': f'Bearer {_get_jwt_token()}'}
            )
            response.raise_for_status()

            for episode in response.json()['data']:
                episodes.append(Episode(
                    database=self.name,
                    id=episode['id'],
                    title=episode['episodeName'],
                    season_number=episode['airedSeason'],
                    episode_number=episode['airedEpisodeNumber'],
                    date=date.fromisoformat(episode['firstAired']),  # TODO
                    series=series,
                ))

            last = response.json()['links']['last']
            page = response.json()['links']['next']

        series.episodes = episodes
        return series

    def search(self, query: str) -> list:
        response = requests.get(
            f'{API_ROOT}/search/series',
            params={'name': query},
            headers={'Authorization': f'Bearer {_get_jwt_token()}'}
        )
        response.raise_for_status()
        return [
            Media(
                database=self.name,
                title=k['seriesName'],
                id=k['id'],
                date=None,
            )
            for k in response.json()['data']
        ]
