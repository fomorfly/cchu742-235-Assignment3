from werkzeug.security import generate_password_hash, check_password_hash

from cs235flix.adapters.repository import AbstractRepository
import cs235flix.adapters.repository as repo
from cs235flix.domain.model import User


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


def add_user(username: str, password: str):
    # Check that username is unique
    user = repo.repo_instance.get_user(username)
    if user is not None:
        raise NameNotUniqueException

    # Encrypt password
    password_hash = generate_password_hash(password)

    user = User(username, password_hash)
    repo.repo_instance.add_user(user)


def get_user(username: str):
    user = repo.repo_instance.get_user(username)
    if user is None:
        raise UnknownUserException

    return user_to_dict(user)


def authenticate_user(username: str, password: str):
    authenticated = False
    user = repo.repo_instance.get_user(username)
    if user is not None:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException


def user_to_dict(user: User):
    user_dict = {
        'username': user.user_name,
        'password': user.password
    }
    return user_dict
