from dataclasses import dataclass


@dataclass
class Media:
    database: str
    title: str
    # language: str
    id: int
    overview: str
    rating: float


@dataclass
class Episode(Media):
    series_id: int
    episode_number: int
    season_number: int


@dataclass
class Series(Media):
    episodes: list


@dataclass
class Movie(Media):
    pass


class Provider:
    def search(query: str) -> Media:
        raise NotImplementedError()
