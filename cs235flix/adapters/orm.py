from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from cs235flix.domain import model

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

genres = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('genre_name', String(255))
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', ForeignKey('users.username')),
    Column('movie_id', ForeignKey('movies.id')),
    Column('review_text', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

actors = Table(
    'actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('actor_full_name', String(255), nullable=False)
)

movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('release', String, nullable=False),
    Column('title', String(255), nullable=False),
    Column('description', String(2048)),
    Column('runtime_minutes', Integer),
    Column('director', String(255), nullable=True)
)

movies_actors = Table(
    'movies_actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('actor_id', ForeignKey('actors.id'))
)

movies_genres = Table(
    'movies_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('genre_id', ForeignKey('genres.id'))
)

movies_users = Table(
    'movies_users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('user_id', ForeignKey('users.id'))
)


def map_model_to_tables():
    mapper(model.Review, reviews, properties={
        '_Review__review_text': reviews.c.review_text,
        '_Review__timestamp': reviews.c.timestamp,
    })

    # mapper(model.Director, directors, properties={
    #     '_director_full_name': directors.c.director_full_name
    # })

    actors_mapper = mapper(model.Actor, actors, properties={
        '_Actor__actor_full_name': actors.c.actor_full_name
    })

    genres_mapper = mapper(model.Genre, genres, properties={
        '_Genre__genre_name': genres.c.genre_name
    })

    movies_mapper = mapper(model.Movie, movies, properties={
        '_Movie__id': movies.c.id,
        '_Movie__release': movies.c.release,
        '_Movie__title': movies.c.title,
        '_Movie__description': movies.c.description,
        '_Movie__director': movies.c.director,
        '_Movie__reviews': relationship(model.Review, backref='_movie'),
        '_Movie__runtime_minutes': movies.c.runtime_minutes,
        '_Movie__actors': relationship(
            actors_mapper,
            secondary=movies_actors,
            backref='_movie'
        ),
        '_Movie__genres': relationship(
            genres_mapper,
            secondary=movies_genres,
            backref='_movie'
        )
    })

    mapper(model.User, users, properties={
        '_User__user_name': users.c.username,
        '_User__password': users.c.password,
        '_User__reviews': relationship(model.Review, backref='_user'),
        '_User__watchlist': relationship(
            movies_mapper,
            secondary=movies_users,
            backref='_user'
        )
    })

