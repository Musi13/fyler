import dataclasses
from dataclasses import dataclass


@dataclass
class Media:
    database: str
    title: str
    # language: str
    id: int
    overview: str
    rating: float

    # I wish dataclasses had this interface naturally,
    # it's a bit more convenient imo.
    def asdict(self):
        return dataclasses.asdict(self)

    def astuple(self):
        return dataclasses.astuple(self)


@dataclass
class Series(Media):
    episodes: list


@dataclass
class Episode(Media):
    series: Series
    episode_number: int
    season_number: int


@dataclass
class Movie(Media):
    pass


class Provider:
    def search(self, query: str) -> list:
        raise NotImplementedError()
