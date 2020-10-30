import csv

from cs235flix.adapters.repository import AbstractRepository
from cs235flix.domain.model import *


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self._movies = []
        self._genres = []
        self._user = []

    def add_movie(self, movie):
        self._movies.append(movie)

    def get_movies(self):
        return self._movies

    def add_user(self, user: User):
        self._user.append(user)

    def get_user(self, username):
        for user in self._user:
            if user.user_name == username:
                return user
        return None

    # Unused
    def add_genre(self, genre):
        self._genres.append(genre)

    def update_user_watchlist(self, user, movie):
        raise NotImplementedError

    def update_movie_review(self, movie, review):
        raise NotImplementedError


def populate(data_path: str, repo: MemoryRepository):
    file_reader = MovieFileCSVReader(data_path)
    file_reader.read_csv_file()

    for mov in file_reader.dataset_of_movies:
        repo.add_movie(mov)

    for gen in file_reader.dataset_of_genres:
        repo.add_genre(gen)


