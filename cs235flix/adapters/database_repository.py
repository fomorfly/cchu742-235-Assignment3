import csv
import os

from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.engine import Engine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug.security import generate_password_hash

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from cs235flix.domain.model import User, Movie, Review, Actor, Director, MovieFileCSVReader
from cs235flix.adapters.repository import AbstractRepository

tags = None


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_movie(self, movie):
        return NotImplementedError

    def get_movies(self) -> User:
        movies = self._session_cm.session.query(Movie)
        return movies

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter_by(_User__user_name=username).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_genre(self, genre):
        raise NotImplementedError

    def update_user_watchlist(self, user: User, movie: Movie):

        with self._session_cm as scm:
            scm.session.add(user)
            scm.session.add(movie)
            scm.commit()


    def update_movie_review(self, movie: Movie, review: Review):
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()


def populate(session_factory, data_path):
    filename = data_path
    movie_file_reader = MovieFileCSVReader(filename)
    movie_file_reader.read_csv_file()

    session = session_factory()

    # This takes all movies from the csv file (represented as domain model objects) and adds them to the
    # database. If the uniqueness of directors, actors, genres is correctly handled, and the relationships
    # are correctly set up in the ORM mapper, then all associations will be dealt with as well!
    for movie in movie_file_reader.dataset_of_movies:
        session.add(movie)
    session.commit()

