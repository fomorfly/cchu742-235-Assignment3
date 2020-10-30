import datetime
import csv


class Director:

    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    def __repr__(self):
        return f"<Director {self.__director_full_name}>"

    def __eq__(self, other):
        if self.__director_full_name == other.director_full_name:
            return True
        return False

    def __lt__(self, other):
        # TODO
        if self.__director_full_name < other.director_full_name:
            return True
        return False

    def __hash__(self):
        # TODO
        return hash(self.__director_full_name)


class Genre:

    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = genre_name.strip()

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    def __repr__(self):
        return f"<Genre {self.__genre_name}>"

    def __eq__(self, other):
        if self.__genre_name == other.__genre_name:
            return True
        return False

    def __lt__(self, other):
        # TODO
        if self.__genre_name < other.__genre_name:
            return True
        return False

    def __hash__(self):
        # TODO
        return hash(self.__genre_name)


class Actor:

    __colleague = []

    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_full_name.strip()

    def add_actor_colleague(self, colleague):
        self.__colleague.append(colleague)
        colleague.__colleague.append(self)

    def check_if_this_actor_worked_with(self, colleague):
        return colleague in self.__colleague

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    def __repr__(self):
        return f"<Actor {self.__actor_full_name}>"

    def __eq__(self, other):
        if self.__actor_full_name == other.__actor_full_name:
            return True
        return False

    def __lt__(self, other):
        if self.__actor_full_name < other.__actor_full_name:
            return True
        return False

    def __hash__(self):
        return hash(self.__actor_full_name)


class Movie:

    def __init__(self, title: str, release):
        if int(release) < 1900:
            self.__release = None
        else:
            self.__release = release

        if title == "" or type(title) is not str:
            self.__title = None
        else:
            self.__title = title.strip()

        self.__description = ""
        self.__director = None
        self.__actors = []
        self.__genres = []
        self.__runtime_minutes = 0
        self.__reviews = []
        self.__id = None

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def release(self) -> int:
        return self.__release

    @release.setter
    def release(self, year):
        self.__release = year

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, desc):
        self.__description = desc.strip()

    @property
    def director(self) -> str:
        return self.__director

    @director.setter
    def director(self, director):
        self.__director = director

    @property
    def actors(self) -> list:
        return self.__actors

    @property
    def genres(self) -> list:
        return self.__genres

    @property
    def reviews(self) -> list:
        return self.__reviews

    @property
    def runtime_minutes(self) -> int:
        return self.__runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, runtime):
        if type(runtime) != int or runtime <= 0:
            raise ValueError
        else:
            self.__runtime_minutes = runtime

    def __repr__(self):
        return f"<Movie {self.__title + ', ' + str(self.__release)}>"

    def __eq__(self, other):
        if self.__title == other.__title and self.__release == other.__release:
            return True
        return False

    def __lt__(self, other):
        if self.__title < other.__title:
            return True
        elif self.__title == other.__title:
            if self.__release < other.__release:
                return True
        else:
            return False

    def __hash__(self):
        return hash(self.__title + str(self.__release))

    def add_actor(self, actor):
        self.__actors.append(actor)

    def remove_actor(self, actor):
        if actor in self.__actors:
            self.__actors.remove(actor)

    def add_genre(self, genre):
        self.__genres.append(genre)

    def add_review(self, review):
        self.__reviews.append(review)

    def remove_review(self, review):
        self.__reviews.remove(review)

    def remove_genre(self, genre):
        if genre in self.__genres:
            self.__genres.remove(genre)


class MovieFileCSVReader:

    def __init__(self, file_name):
        self.__filename = file_name
        self.__dataset_of_movies = []
        self.__dataset_of_actors = set([])  # unique actor, make sure its Actor()
        self.__dataset_of_directors = set([])  # unique, one director can direct many movies
        self.__dataset_of_genres = set([])  # unique, one genre many movies

    @property
    def dataset_of_movies(self):
        return self.__dataset_of_movies

    @property
    def dataset_of_actors(self):
        return self.__dataset_of_actors

    @property
    def dataset_of_directors(self):
        return self.__dataset_of_directors

    @property
    def dataset_of_genres(self):
        return self.__dataset_of_genres

    def read_csv_file(self):
        with open(self.__filename, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            id = 0
            for movie in reader:
                actorStr = movie["Actors"]
                actorStrList = actorStr.split(",")
                for actor in actorStrList:
                    self.__dataset_of_actors.add(Actor(actor.strip()))

                self.__dataset_of_directors.add(Director(movie["Director"]))

                genreStr = movie["Genre"]
                genreStrList = genreStr.split(",")
                for genre in genreStrList:
                    self.__dataset_of_genres.add(Genre(genre))

                # dataset of genres, actors, and directors done
                # start reading movies
                app_movie = Movie(movie["Title"], str(movie["Year"]))
                app_movie.id = id
                id = id + 1
                app_movie.director = movie["Director"]

                genre_list = movie["Genre"].split(",")
                for genre in genre_list:
                    for gen in self.__dataset_of_genres:
                        if gen.genre_name == genre.strip():
                            app_movie.add_genre(gen)
                            continue

                actor_list = movie["Actors"].split(",")
                for actor_name in actor_list:
                    for actor in self.dataset_of_actors:
                        if actor.actor_full_name == actor_name.strip():
                            app_movie.add_actor(actor)
                            continue

                app_movie.description = movie["Description"]
                app_movie.runtime_minutes = int(movie["Runtime (Minutes)"])
                self.__dataset_of_movies.append(app_movie)


        return


class Review:

    def __init__(self, movie, review_text, username):
        self.__movie = movie
        self.__review_text = review_text
        # if rating < 1 or rating > 10:  # should be between 1 and 10?
        #     self.__rating = None
        # else:
        #     self.__rating = rating
        self.__username = username
        self.__timestamp = datetime.datetime.now()

    @property
    def username(self):
        return self.__username

    @property
    def movie(self):
        return self.__movie

    @property
    def review_text(self):
        return self.__review_text

    # @property
    # def rating(self):
    #     return self.__rating

    @property
    def timestamp(self):
        return self.__timestamp

    def __repr__(self):
        return self.__movie + ", " + self.__review_text

    def __eq__(self, other):
        if self.__movie == other.__movie and self.__review_text == other.__review_text \
                and self.__timestamp == other.__timestamp:
            return True
        return False


class User:

    def __init__(self, username, password):
        self.__user_name = username.strip().lower()
        self.__password = password
        self.__watched_movies = []
        self.__reviews = []
        self.__watchlist = []       # stores a list of movie obj
        self.__time_spent_watching_movies_minutes = 0  # NON NEGATIVE

    @property
    def user_name(self):
        return self.__user_name

    @property
    def password(self):
        return self.__password

    @property
    def watched_movies(self):
        return self.__watched_movies

    @property
    def reviews(self):
        return self.__reviews

    @property
    def watchlist(self):
        return self.__watchlist

    @property
    def time_spent_watching_movies_minutes(self):
        return self.__time_spent_watching_movies_minutes

    def __repr__(self):
        return f"<User {self.__user_name}>"

    def __eq__(self, other):
        return self.__user_name == other.__user_name

    def __lt__(self, other):
        return self.__user_name < other.__user_name

    def __hash__(self):
        return hash(self.__user_name)

    def watch_movie(self, movie):
        self.__watched_movies.append(movie)
        self.__time_spent_watching_movies_minutes = self.__time_spent_watching_movies_minutes + movie.runtime_minutes

    def add_review(self, review):
        self.__reviews.append(review)

    def add_watchlist(self, movie):
        self.__watchlist.append(movie)

    def del_watchlist(self, movie):
        for i in range(0, len(self.watchlist)):
            if self.watchlist[i] == movie:
                popped = self.watchlist.pop(i)
        return

    # def delete_watchlist
