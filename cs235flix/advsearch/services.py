import math

from flask import Blueprint, render_template, url_for
import cs235flix.adapters.repository as repo


# splits a string into a list of data saperated by commas in lower case, eg. "a, B, c" -> [a, b, c]
def process_to_list(data: str):
    if len(data) <= 0:
        return None
    data_split = data.split(",")
    for i in range(len(data_split)):
        data_split[i] = data_split[i].strip()
        data_split[i] = data_split[i].lower()
    return data_split


def get_filtered_movies(genre_list, director_list, actor_list):
    movie_list = repo.repo_instance.get_movies()
    filtered_movies = []
    for movie in movie_list:
        match_genre = True
        match_director = True
        match_actor = True

        # work with genre
        if genre_list != None:
            movie_genre_list = genre_to_str(movie.genres)
            for filter_genre in genre_list:
                if filter_genre not in movie_genre_list:
                    match_genre = False
                    break

        #work with director
        if director_list != None:
            director_str = director_to_str(movie.director)
            if director_str not in director_list:
                match_director = False

        #work with actor
        if actor_list != None:
            movie_actor_list = actor_to_str(movie.actors)
            for filter_actor in actor_list:
                if filter_actor not in movie_actor_list:
                    match_actor = False
                    break

        if match_actor and match_genre and match_director:
            filtered_movies.append(movie)

    return filtered_movies


def get_page(page_no: int, movie_list, num_per_page=20):
    mov_num = page_no * num_per_page
    movie_showed = movie_list[mov_num: mov_num + num_per_page]
    return movie_showed


def add_movies_in_dict(movie_list):
    movie_dict_list = []

    for movie in movie_list:
        movie_dict = {"movie": movie}
        movie_dict_list.append(movie_dict)
    return movie_dict_list


# returns an int representing total number of pages
def get_max_page(movie_list, num_per_page=20):
    total_movies = len(movie_list)
    total_pages = total_movies / num_per_page
    total_pages = math.ceil(total_pages)
    return total_pages


# [Genre] -> [str.lower()]
def genre_to_str(genre_list):
    str_list = []
    for genre in genre_list:
        str_list.append(genre.genre_name.lower())
    return str_list


def director_to_str(director):
    director_str = director.lower()
    return director_str


def actor_to_str(director_list):
    str_list = []
    for actor in director_list:
        str_list.append(actor.actor_full_name.lower())
    return str_list


