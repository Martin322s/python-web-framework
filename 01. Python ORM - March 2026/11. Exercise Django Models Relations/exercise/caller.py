import os
from datetime import timedelta, date, datetime

import django
from django.utils.timezone import now

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from datetime import timedelta
from django.db.models import F, ExpressionWrapper, DateField
from main_app.models import Author, Song, Artist, Product, Review, DrivingLicense, Registration, Car, Owner


# Create queries within functions
def show_all_authors_with_their_books():
    authors = Author.objects.all()
    authors_with_books = []

    for author in authors:
        books = author.book_set.all()

        if not books:
            continue

        titles = ', '.join(book.title for book in books)

        authors_with_books.append(f"{author.name} has written - {titles}!")

    return "\n".join(authors_with_books)

def delete_all_authors_without_books():
    authors = Author.objects.all()

    for author in authors:
        books = author.book_set.all()

        if not books:
            author.delete()

def add_song_to_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.add(song)
    artist.save()

def get_songs_by_artist(artist_name: str):
    artist = Artist.objects.get(name=artist_name)
    songs = artist.songs.all().order_by("-id")

    return songs

def remove_song_from_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.remove(song)

def calculate_average_rating_for_product_by_name(product_name: str):
    product = Product.objects.get(name=product_name)
    reviews = product.reviews.all()

    return sum(r.rating for r in reviews) / len(reviews)

def get_reviews_with_high_ratings(threshold: int):
    reviews = Review.objects.filter(rating__gte=threshold)
    return reviews

def get_products_with_no_reviews():
    products = Product.objects.filter(reviews__isnull=True).order_by("-name")
    return products

def delete_products_without_reviews():
    products = Product.objects.all()

    for product in products:
        if not product.reviews.all():
            product.delete()

def calculate_licenses_expiration_dates():
    licenses = DrivingLicense.objects.order_by("-license_number")
    return "\n".join(str(l) for l in licenses)

def get_drivers_with_expired_licenses(due_date: date):
    licenses = DrivingLicense.objects.all()
    expired_licenses = []

    for l in licenses:
        if l.expiration_date < due_date:
            expired_licenses.append(l.driver)
    return expired_licenses

def register_car_by_owner(owner):
    car = Car.objects.filter(registration__isnull=True).first()
    registration = Registration.objects.filter(car__isnull=True).first()

    car.owner = owner
    car.registration = registration
    registration.registration_date = datetime.today()
    registration.car = car
    car.save()
    registration.save()

    return f"Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}."

