from better_profanity import profanity
from flask import Blueprint
from flask import request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import cs235flix.home.services as services
from cs235flix.authentication.authentication import login_required

page = 0

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    global page
    page = 0
    movie_showed = services.get_page(page)
    mov_dict_list = services.add_movies_in_dict(movie_showed)  # adds each movies in movie_showed into a saperate dicts
    for movie_dict in mov_dict_list:
        movie_dict["view_movie_url"] = url_for("home_bp.view_movie", movie_id=movie_dict["movie"].id)
    return render_template(
        'home/home.html',
        movies=mov_dict_list,
        prev_home_url=url_for('home_bp.prev_home'),
        next_home_url=url_for('home_bp.next_home')
    )


@home_blueprint.route('/next_home', methods={'GET'})
def next_home():
    global page
    page = page + 1
    if page >= services.get_max_page():
        page = page - 1
    movie_showed = services.get_page(page)
    mov_dict_list = services.add_movies_in_dict(movie_showed)
    for movie_dict in mov_dict_list:
        movie_dict["view_movie_url"] = url_for("home_bp.view_movie", movie_id=movie_dict["movie"].id)
    return render_template(
        "home/home.html",
        prev_home_url=url_for('home_bp.prev_home'),
        next_home_url=url_for('home_bp.next_home'),
        movies=mov_dict_list
    )


@home_blueprint.route('/prev_home', methods={'GET'})
def prev_home():
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
        prev_home_url=url_for('home_bp.prev_home'),
        next_home_url=url_for('home_bp.next_home'),
        movies=mov_dict_list
    )


@home_blueprint.route('/view_movie', methods={'GET'})
def view_movie():
    try:
        username = session["username"]
        user = services.get_user(username)
    except:
        user = None

    # movie_dict = request.args.get('movie_dict')
    movie_id = request.args.get('movie_id')
    movie = services.get_movie_with_index(movie_id)  # id represents the index in this case
    review_movie = url_for(("home_bp.review_movie"), movie_id=movie_id)
    add_to_watchlist = url_for(("watchlist_bp.add_to_watchlist"), movie_id=movie_id)

    if user is None or movie not in user.watchlist:
        watchlist_label = "Add to Watchlist"
    else:
        watchlist_label = "Remove from Watchlist"

    # movie_dict = {}
    #
    # movie_dict["view_movie_url"] = url_for("home_bp.view_movie", movie_id=movie_dict["movie"].id)
    # movie_dict["review_movie_url"] = url_for(("home_bp.review_movie"), movie_id=movie_dict["movie"].id)
    return render_template(
        "home/view_movie.html",
        movie=movie,
        review_movie=review_movie,
        add_to_watchlist=add_to_watchlist,
        add_watchlist_label = watchlist_label
    )


@home_blueprint.route('/review', methods={'GET', 'POST'})
@login_required
def review_movie():
    # Obtain the username of the currently logged in user.
    username = session['username']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an article id, when subsequently called with a HTTP POST request, the article id remains in the
    # form.
    form = ReviewForm()

    if form.validate_on_submit():
        movie_id = int(form.movie_id.data)

        services.add_review(movie_id, form.review.data, username)

        return redirect(url_for('home_bp.view_movie', movie_id=movie_id))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the article id, representing the article to comment, from a query parameter of the GET request.
        movie_id = int(request.args.get('movie_id'))

        # Store the movie id in the form.
        form.movie_id.data = movie_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the article id of the article being commented from the form.
        movie_id = int(form.movie_id.data)

    # For a GET or an unsuccessful POST, retrieve the article to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    movie = services.get_movie_with_index(movie_id)
    return render_template(
        'home/review_movie.html',
        movie=movie,
        form=form,
        handler_url=url_for('home_bp.review_movie'),
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    movie_id = HiddenField("Movie id")
    submit = SubmitField('Submit')