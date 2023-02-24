from flask import Flask
from flask_restx import Api

from config import Config
from dao.model.director import Director
from dao.model.genre import Genre
from dao.model.movie import Movie
from helpers.constants import DATA
from setup_db import db
from views.auth import auth_ns
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movie_ns
from views.users import user_ns


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(user_ns)
    create_data(app, db)


def create_data(app, db):
    with app.app_context():
        db.drop_all()
        db.create_all()

        data = DATA

        for movie in data["movies"]:
            m = Movie(
                id=movie["pk"],
                title=movie["title"],
                description=movie["description"],
                trailer=movie["trailer"],
                year=movie["year"],
                rating=movie["rating"],
                genre_id=movie["genre_id"],
                director_id=movie["director_id"],
            )
            db.session.add(m)
            db.session.commit()

        for director in data["directors"]:
            d = Director(
                id=director["pk"],
                name=director["name"],
            )
            db.session.add(d)
            db.session.commit()

        for genre in data["genres"]:
            d = Genre(
                id=genre["pk"],
                name=genre["name"],
            )
            db.session.add(d)
            db.session.commit()


if __name__ == '__main__':
    app = create_app(Config())
    app.run(debug=True)
