import requests
import json

from . import provider

API_ROOT = 'https://graphql.anilist.co/'


class AniListProvider(provider.Provider):
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
            print(result)
            ret.append(
                provider.Series(
                    database='AniList',
                    title=result['title']['romaji'],
                    id=result['id'],
                    overview=None,
                    rating=None,
                    episodes=[],
                ))

        return ret
