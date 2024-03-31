from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm

# Create your views here.


def place_list(request):  # this view handles requests to home page

    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST)  # create form with form data sent in request
        place = form.save()  # make Place model object
        if form.is_valid():  # if user entered valid info - django automatically validates using DB constraints
            place.save()  # save the place to the DB
            return redirect('place_list')  # reload place_list

    # handle a GET request

    # make database query
    # filter and fetch unvisited Place objects from database and put into places list, sorted by name
    places = Place.objects.filter(visited=False).order_by('name')

    # create new place form
    new_place_form = NewPlaceForm()

    # renders/combines wishlist.html template, new place form, and list of Place objects to build webpage
    return render(request, 'travel_wishlist/wishlist.html',
                  {'places': places, 'new_place_form': new_place_form})


def places_visited(request):  # handles requests to visited page

    # database query
    # filter and fetch visited Place objects from database and put into visited list, sorted by name
    visited = Place.objects.filter(visited=True).order_by('name')

    return render(request, 'travel_wishlist/visited.html', {'visited': visited})


def place_was_visited(request, place_pk):  # django extracts number from path to get place_pk

    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk)  # database query to get visited place matching the primary key
        place = get_object_or_404(Place, pk=place_pk)  # try to get object or return 404 error response
        place.visited = True  # can manipulate fields of model objects within views
        place.save()  # save DB

    #  return redirect('places_visited')  # redirect to places visited page
    return redirect('place_list')  # reload wishlist page


def about(request):  # handles requests to about page
    author = 'Alexandrea'
    about = 'A website to create a list of places to visit'

    # combines about.html template with author and about data
    return render(request, 'travel_wishlist/about.html',
                  {'author': author, 'about': about})


