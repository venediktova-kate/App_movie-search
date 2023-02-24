from dao.model.movie import Movie


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(Movie).get(bid)

    def get_all(self):
        return self.session.query(Movie).all()

    def get_by_status(self, status):
        if status == 'new':
            return self.session.query(Movie).order_by(Movie.year.desc()).all()
        else:
            return self.session.query(Movie).all()

    def get_by_page(self, page):
        return self.session.query(Movie).offset(12 * (int(page) - 1)).limit(12).all()

    def get_by_status_and_page(self, status, page):
        if status == 'new':
            return self.session.query(Movie).order_by(Movie.year.desc()).offset(12 * (int(page) - 1)).limit(12).all()
        else:
            return self.session.query(Movie).all()
