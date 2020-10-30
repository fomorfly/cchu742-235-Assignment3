import math

from flask import Blueprint, render_template, url_for, session
import cs235flix.adapters.repository as repo
from cs235flix.domain.model import User
from cs235flix.domain.model import Review


def get_page(page_no: int, num_per_page=20):
    mov_num = page_no * num_per_page
    username = session["username"]
    user = repo.repo_instance.get_user(username)
    movie_list = user.watchlist
    movie_showed = movie_list[mov_num: mov_num + num_per_page]
    return movie_showed


def get_movie_with_index(index):
    username = session["username"]
    user = repo.repo_instance.get_user(username)
    movie_list = user.watchlist
    return movie_list[int(index)]


def add_movies_in_dict(movie_list):
    movie_dict_list = []

    for movie in movie_list:
        movie_dict = {}
        movie_dict["movie"] = movie
        movie_dict_list.append(movie_dict)
    return movie_dict_list


# returns an int representing total number of pages
def get_max_page(num_per_page=20):
    username = session["username"]
    user = repo.repo_instance.get_user(username)
    total_movies = len(user.watchlist)
    total_pages = total_movies / num_per_page
    total_pages = math.ceil(total_pages)
    return total_pages


def get_movie(movie_id):
    for movie in repo.repo_instance.get_movies():
        if movie.id == movie_id:
            return movie
    return None


def get_user(username):
    user = repo.repo_instance.get_user(username)
    return user


def del_watchlist(movie, user):
    user.del_watchlist(movie)
    repo.repo_instance.update_user_watchlist(user, movie)
    return


def add_watchlist(movie, user):
    user.add_watchlist(movie)
    repo.repo_instance.update_user_watchlist(user, movie)
    return