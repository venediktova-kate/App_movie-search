from dao.movie import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self, filters):
        if filters.get("status") is not None and filters.get("page") is not None:
            movies = self.dao.get_by_status_and_page(filters.get('status'), filters.get('page'))
        elif filters.get("status") is not None:
            movies = self.dao.get_by_status(filters.get("status"))
        elif filters.get("page") is not None:
            movies = self.dao.get_by_page(filters.get("page"))
        else:
            movies = self.dao.get_all()
        return movies
