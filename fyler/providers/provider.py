from fyler.models import Media


class Provider:
    def detail(self, media: Media) -> Media:
        raise NotImplementedError()

    def search(self, query: str) -> list:
        raise NotImplementedError()
