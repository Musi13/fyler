from fyler.models import Media


class Provider:
    def detail(self, media: Media) -> Media:
        """Add more detail to a search result"""
        raise NotImplementedError()

    def search(self, query: str) -> list:
        """Search for a query and return a list of Media results"""
        raise NotImplementedError()
