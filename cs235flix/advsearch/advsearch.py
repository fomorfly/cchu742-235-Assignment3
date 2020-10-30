from flask import Blueprint, render_template, url_for, request
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import TextAreaField, SubmitField

import cs235flix.advsearch.services as services

advsearch_blueprint = Blueprint(
    'advsearch_bp', __name__, url_prefix='/advsearch')

chosen_genres = []
chosen_directors = []
chosen_actors = []
chosen_movies = list()
page = 0


@advsearch_blueprint.route('/advsearch', methods={'GET', 'POST'})
def advsearch():
    global chosen_genres
    global chosen_directors
    global chosen_actors
    global chosen_movies

    form = SearchForm()

    if form.validate_on_submit():
        genre_list = services.process_to_list(form.genre.data)
        chosen_genres = genre_list
        director_list = services.process_to_list(form.director.data)
        chosen_directors = director_list
        actor_list = services.process_to_list(form.actor.data)
        chosen_directors = actor_list
        chosen_movies = services.get_filtered_movies(genre_list, director_list, actor_list)
        return redirect(url_for('advsearch_bp.advsearch_results'))
    else:
        opt_msg = request.args.get('opt_msg')
        if opt_msg == None:
            opt_msg = ''
    return render_template(
        "advsearch/advsearch.html",
        form=form,
        handler_url=url_for('advsearch_bp.advsearch'),
        opt_msg=opt_msg
    )


@advsearch_blueprint.route('/results', methods={'GET'})
def advsearch_results():
    global page
    global chosen_movies
    page = 0
    if len(chosen_movies) <= 0:
        msg = "Oops, we couldn't find what you were looking for. Either we don't have it or you have spelled something wrongly. Please check your spelling and try again."
        return redirect(url_for('advsearch_bp.advsearch', opt_msg=msg))
    movie_showed = services.get_page(page, chosen_movies)
    mov_dict_list = services.add_movies_in_dict(movie_showed)
    for movie_dict in mov_dict_list:
        movie_dict["view_movie_url"] = url_for("home_bp.view_movie", movie_id=movie_dict["movie"].id)
    return render_template(
        'home/home.html',
        movies=mov_dict_list,
        prev_home_url=url_for('advsearch_bp.prev_advsearch_results'),
        next_home_url=url_for('advsearch_bp.next_advsearch_results')
    )


@advsearch_blueprint.route('/next_results', methods={'GET'})
def next_advsearch_results():
    global page
    global chosen_movies
    page = page + 1
    # no more than 50 pages
    if page >= services.get_max_page(chosen_movies):
        page = page - 1
    movie_showed = services.get_page(page, chosen_movies)
    mov_dict_list = services.add_movies_in_dict(movie_showed)
    for movie_dict in mov_dict_list:
        movie_dict["view_movie_url"] = url_for("home_bp.view_movie", movie_id=movie_dict["movie"].id)
    return render_template(
        "home/home.html",
        prev_home_url=url_for('advsearch_bp.prev_advsearch_results'),
        next_home_url=url_for('advsearch_bp.next_advsearch_results'),
        movies=mov_dict_list
    )


@advsearch_blueprint.route('/prev_results', methods={'GET'})
def prev_advsearch_results():
    global page
    global chosen_movies
    page = page - 1
    if page < 0:
        page = 0
    movie_showed = services.get_page(page, chosen_movies)
    mov_dict_list = services.add_movies_in_dict(movie_showed)
    for movie_dict in mov_dict_list:
        movie_dict["view_movie_url"] = url_for("home_bp.view_movie", movie_id=movie_dict["movie"].id)
        movie_dict["review_movie_url"] = url_for(("home_bp.review_movie"), movie_id=movie_dict["movie"].id)
    return render_template(
        "home/home.html",
        prev_home_url=url_for('advsearch_bp.prev_advsearch_results'),
        next_home_url=url_for('advsearch_bp.next_advsearch_results'),
        movies=mov_dict_list
    )


class SearchForm(FlaskForm):
    director = TextAreaField('Search By Director', [])
    genre = TextAreaField('Search By Genre', [])
    actor = TextAreaField('Search By Actor', [])
    submit = SubmitField('Search')
