import math

from flask import Blueprint, render_template, url_for
import cs235flix.adapters.repository as repo
from cs235flix.domain.model import Review


def get_page(page_no: int, num_per_page=20):
    mov_num = page_no * num_per_page
    movie_list = repo.repo_instance.get_movies()
    movie_showed = movie_list[mov_num: mov_num + 20]
    return movie_showed


def get_movie_with_index(index):
    movie_list = repo.repo_instance.get_movies()
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
    total_movies = len(repo.repo_instance.get_movies())
    total_pages = total_movies / num_per_page
    total_pages = math.ceil(total_pages)
    return total_pages


def add_review(movie_id, review_txt, username):
    # movie_list = repo.repo_instance.get_movies()
    movie = get_movie(movie_id)
    review = Review(movie, review_txt, username)
    movie.add_review(review)
    repo.repo_instance.update_movie_review(movie, review)


def get_user(username):
    user = repo.repo_instance.get_user(username)
    return user


def get_movie(movie_id):
    for movie in repo.repo_instance.get_movies():
        if movie.id == movie_id:
            return movie
    return None


def del_watchlist(movie, user):
    user.del_watchlist(movie)
    repo.repo_instance.update_user_watchlist(user, movie)
    return
