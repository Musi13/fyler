import requests
import json

from . import provider

API_ROOT = 'https://graphql.anilist.co/'


class AniListProvider(provider.Provider):
    name = 'AniList'

    def detail(self, series: provider.Series) -> provider.Series:
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
                  coverImage {
                    medium
                    large
                    extraLarge
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
                provider.Series(
                    database=self.name,
                    title=result['title']['romaji'],
                    id=result['id'],
                    overview=None,
                    rating=None,
                    episodes=[],
                ))

        return ret
