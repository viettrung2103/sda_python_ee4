from django.http import HttpResponse
from viewer.models import Genre


def welcome(request, s):
    city = request.GET.get('city', '')
    return HttpResponse(f"Welcome to Viewer app, {s}! Very good to have you in {city}")


def sum_numbers(request):
    number1 = request.GET.get('value1', 0)
    number2 = request.GET.get('value2', 0)
    result = int(number1) + int(number2)

    return HttpResponse(f"The sum for numbers {number1} and {number2} is {result}")


def create_genre(request):

    name_request = request.GET.get('name', None)

    if name_request is None:
        return HttpResponse("Please, give a valid name for the genre in the query string 'name'")

    genre = Genre.objects.create(name=name_request)

    return HttpResponse(f"Genre has been created with id {genre.id}")


def update_genre(request, s):
    name_request = request.GET.get('name', None)

    genre = Genre.objects.get(id=int(s))
    genre.name = name_request
    genre.save()

    return HttpResponse(f"The genre has been updated to {genre.name}")


def delete_genre(request, s):

    if not Genre.objects.filter(id=int(s)).exists():
        return HttpResponse(f"The genre with id {s} does not exist")

    Genre.objects.get(id=int(s)).delete()

    return HttpResponse(f"The genre with id {s} has been removed")


def list_genre(request):

    name_filter = request.GET.get('name', None)
    is_favorite_filter = request.GET.get('favorite', None)

    genres = Genre.objects.all()
    if name_filter:
        genres = genres.filter(name__startswith=name_filter)

    if is_favorite_filter:
        genres = genres.filter(is_favorite=is_favorite_filter)

    genre_response = ""
    for genre in genres:
        genre_row = f"<b> {genre.name} </b>(<i>{genre.is_favorite}</i>)<br>"
        genre_response = genre_response + genre_row

    return HttpResponse(f"List of genres: <br> {genre_response}")