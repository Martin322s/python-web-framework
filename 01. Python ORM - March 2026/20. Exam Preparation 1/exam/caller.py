import os
import django
from django.db.models import Q, Count, Avg, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Movie, Actor, Director
from datetime import date
from decimal import Decimal

# Create queries within functions
def populate_db():
    director_1 = Director.objects.create(
        full_name="Christopher Nolan",
        birth_date=date(1970, 7, 30),
        nationality="British-American",
        years_of_experience=25,
    )

    director_2 = Director.objects.create(
        full_name="Steven Spielberg",
        birth_date=date(1946, 12, 18),
        nationality="American",
        years_of_experience=40,
    )

    actor_1 = Actor.objects.create(
        full_name="Leonardo Di Caprio",
        birth_date=date(1974, 11, 11),
        nationality="American",
        is_awarded=True,
    )

    actor_2 = Actor.objects.create(
        full_name="Matthew McNaught",
        birth_date=date(1969, 11, 4),
        nationality="American",
        is_awarded=True,
    )

    actor_3 = Actor.objects.create(
        full_name="Tom Hanks",
        birth_date=date(1956, 7, 9),
        nationality="American",
        is_awarded=True,
    )

    movie_1 = Movie.objects.create(
        title="Inception",
        release_date=date(2010, 7, 16),
        storyline="A thief enters dreams to steal secrets.",
        genre="Action",
        rating=Decimal("8.8"),
        is_classic=True,
        is_awarded=True,
        director=director_1,
        starring_actor=actor_1,
    )

    movie_2 = Movie.objects.create(
        title="Interstellar",
        release_date=date(2014, 11, 7),
        storyline="A team travels through a wormhole to save humanity.",
        genre="Drama",
        rating=Decimal("8.6"),
        is_classic=False,
        is_awarded=True,
        director=director_1,
        starring_actor=actor_2,
    )

    movie_3 = Movie.objects.create(
        title="Saving Private Ryan",
        release_date=date(1998, 7, 24),
        storyline="A group of soldiers searches for a paratrooper during WWII.",
        genre="Drama",
        rating=Decimal("8.7"),
        is_classic=True,
        is_awarded=True,
        director=director_2,
        starring_actor=actor_3,
    )

    movie_1.actors.add(actor_1, actor_2)
    movie_2.actors.add(actor_1, actor_2)
    movie_3.actors.add(actor_3, actor_1)

def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None: return ""

    query = None
    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)

    if search_name is not None and search_nationality is not None:
        query = Q(query_name & query_nationality)
    elif search_name is not None:
        query = Q(query_name)
    elif search_nationality is not None:
        query = Q(query_nationality)

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors: return ""

    result = []

    for director in directors:
        result.append(f"Director: {director.full_name}, nationality: {director.nationality}, experience: {director.years_of_experience}")

    return '\n'.join(result)

def get_top_director():
    director = Director.objects.get_directors_by_movies_count().first()
    if not director: return ""

    return f"Top Director: {director.full_name}, movies: {director.movies_count}."

def get_top_actor():
    actor = Actor.objects.prefetch_related('starring_movies').annotate(
        movies_count=Count('starring_movies'),
        avg_rating=Avg('starring_movies__rating')
    ).order_by('-movies_count', 'full_name').first()

    if not actor or not actor.movies_count:
        return ""

    movies = ', '.join(movie.title for movie in actor.starring_movies.all())

    return (
        f"Top Actor: {actor.full_name}, starring in movies: {movies}, "
        f"movies average rating: {actor.avg_rating:.1f}"
    )

def get_actors_by_movies_count():
    actors = Actor.objects.annotate(
        movies_count=Count('actor_movies')
    ).order_by('-movies_count', 'full_name')[:3]

    if not actors or not actors[0].movies_count: return ""

    result = []

    for actor in actors:
        result.append(f"{actor.full_name}, participated in {actor.movies_count} movies")

    return '\n'.join(result)

def get_top_rated_awarded_movie():
    top_movie = Movie.objects.select_related('starring_actor').prefetch_related('actors').filter(
        is_awarded=True
    ).order_by(
        '-rating', 'title'
    ).first()

    if not top_movie:
        return ""

    starring_actor = top_movie.starring_actor.full_name if top_movie.starring_actor else "N/A"
    participating_actors = top_movie.actors.order_by('full_name').values_list('full_name', flat=True)

    cast = ', '.join(participating_actors)

    return (
        f"Top rated awarded movie: {top_movie.title}, rating: {top_movie.rating}. "
        f"Starring actor: {starring_actor}. Cast: {cast}."
    )

def increase_rating():
    updated_movies = Movie.objects.filter(
        is_classic=True,
        rating__lt=10
    ).update(
        rating=F('rating') + 0.1
    )

    if updated_movies == 0:
        return "No ratings increased."

    return f"Rating increased for {updated_movies} movies."