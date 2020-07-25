import requests
from datetime import date

from .provider import Provider
from fyler.models import Series

API_ROOT = 'https://graphql.anilist.co/'


class AniListProvider(Provider):
    name = "AniList (Doesn't work. No episode data)"

    def detail(self, series: Series) -> Series:
        """Adds more detail to a series, since we don't get everything from a search"""
        detail_qgl = '''
        '''
        return series

    def search(self, query: str) -> list:
        search_gql = '''
            query ($query: String) {
              Page {
                media(search: $query, type: ANIME) {
                  id
                  title {
                    romaji
                    english
                    native
                  }
                  startDate {
                    year
                    month
                    day
                  }
                }
              }
            }
        '''
        body = {
            'query': search_gql,
            'variables': {'query': query}
        }
        response = requests.post(API_ROOT, json=body)
        response.raise_for_status()
        ret = []
        for result, _ in zip(response.json()['data']['Page']['media'], range(5)):
            ret.append(
                Series(
                    database=self.name,
                    title=result['title']['romaji'],
                    id=result['id'],
                    date=date(
                        int(result['startDate']['year']),
                        int(result['startDate']['month']),
                        int(result['startDate']['day']),
                    ),
                    episodes=[],
                ))

        return ret
