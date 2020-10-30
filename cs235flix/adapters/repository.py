import abc

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_movie(self, movie):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username):
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre):
        raise NotImplementedError

    @abc.abstractmethod
    def update_user_watchlist(self, user, movie):
        raise NotImplementedError

    @abc.abstractmethod
    def update_movie_review(self, movie, review):
        raise NotImplementedError

