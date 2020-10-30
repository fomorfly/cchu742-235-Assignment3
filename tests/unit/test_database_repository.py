from datetime import date, datetime

import pytest

from cs235flix.adapters.database_repository import SqlAlchemyRepository
from cs235flix.domain.model import User, Movie, Review, Actor
from cs235flix.adapters.repository import RepositoryException

def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    user2 = repo.get_user('Dave')

    assert user.user_name == user.user_name

def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('fmercury', '8734gfe2058v')
    repo.add_user(user)

    user = repo.get_user('fmercury')
    assert user.user_name == user.user_name

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None

