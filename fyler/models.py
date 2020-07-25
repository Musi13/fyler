import dataclasses
from dataclasses import dataclass


@dataclass
class Media:
    id: int
    database: str
    title: str

    # I wish dataclasses had this interface naturally,
    # it's a bit more convenient imo.
    def asdict(self):
        return dataclasses.asdict(self)

    def astuple(self):
        return dataclasses.astuple(self)

    def template_values(self) -> dict:
        return {
            'id': self.id,
            'db': self.database,
            't': self.title,
        }


@dataclass
class Series(Media):
    episodes: list


@dataclass
class Episode(Media):
    series: Series
    episode_number: int
    season_number: int

    def template_values(self) -> dict:
        return dict(**super().template_values(), **{
            'n': self.series.title,
            's': self.season_number,
            'e': self.episode_number,
            'sxe': f'{self.season_number}x{self.episode_number:02}',
            's00e00': f'S{self.season_number:02}E{self.episode_number:02}' if self.season_number and self.episode_number else '*',
            'e00': f'{self.episode_number:02}',
        })


@dataclass
class Movie(Media):
    pass
