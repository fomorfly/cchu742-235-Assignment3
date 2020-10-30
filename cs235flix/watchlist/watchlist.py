from better_profanity import profanity
from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

import cs235flix.watchlist.services as services
from cs235flix.authentication.authentication import login_required

page = 0

watchlist_blueprint = Blueprint(
    'watchlist_bp', __name__)


@watchlist_blueprint.route('/watchlist', methods=['GET'])
@login_required
def watchlist():
    global page
    page = 0
    movie_showed = services.get_page(page)
    mov_dict_list = services.add_movies_in_dict(movie_showed)
    for movie_dict in mov_dict_list:
        movie_dict["view_movie_url"] = url_for("home_bp.view_movie", movie_id=movie_dict["movie"].id)
    return render_template(
        'home/home.html',
        movies=mov_dict_list,
        prev_home_url=url_for('watchlist_bp.prev_watchlist'),
        next_home_url=url_for('watchlist_bp.next_watchlist'),
    )


@watchlist_blueprint.route('/next_watchlist', methods={'GET'})
def next_watchlist():
    global page
    page = page + 1
    if page > services.get_max_page():
        page = page - 1
    movie_showed = services.get_page(page)
    mov_dict_list = services.add_movies_in_dict(movie_showed)
    for movie_dict in mov_dict_list:
        movie_dict["view_movie_url"] = url_for("home_bp.view_movie", movie_id=movie_dict["movie"].id)
    return render_template(
        "home/home.html",
        prev_home_url=url_for('watchlist_bp.prev_watchlist'),
        next_home_url=url_for('watchlist_bp.next_watchlist'),
        movies=mov_dict_list
    )


@watchlist_blueprint.route('/prev_watchlist', methods={'GET'})
def prev_watchlist():
    global page
    page = page - 1
    if page < 0:
        page = 0
    movie_showed = services.get_page(page)
    mov_dict_list = services.add_movies_in_dict(movie_showed)
    for movie_dict in mov_dict_list:
        movie_dict["view_movie_url"] = url_for("home_bp.view_movie", movie_id=movie_dict["movie"].id)
        movie_dict["review_movie_url"] = url_for(("home_bp.review_movie"), movie_id=movie_dict["movie"].id)
    return render_template(
        "home/home.html",
        prev_home_url=url_for('watchlist_bp.prev_watchlist'),
        next_home_url=url_for('watchlist_bp.next_watchlist'),
        movies=mov_dict_list
    )


@watchlist_blueprint.route('/view_movie/add_to_watchlist', methods={'GET'})
@login_required
def add_to_watchlist():
    username = session["username"]
    user = services.get_user(username)

    movie_id = int(request.args.get('movie_id'))
    movie = services.get_movie(movie_id)

    review_movie = url_for(("home_bp.review_movie"), movie_id=movie_id)
    add_to_watchlist = url_for(("watchlist_bp.add_to_watchlist"), movie_id=movie_id)


    if movie not in user.watchlist:
        services.add_watchlist(movie, user)
        watchlist_label = "Remove from Watchlist"
    else:
        services.del_watchlist(movie, user)
        watchlist_label = "Add to Watchlist"

    return render_template(
        "home/view_movie.html",
        movie=movie,
        review_movie=review_movie,
        add_to_watchlist=add_to_watchlist,
        add_watchlist_label=watchlist_label
    )