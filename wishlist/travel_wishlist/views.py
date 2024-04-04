from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden


# @login_required makes views only accessible if a user is logged in
@login_required
def place_list(request):  # this view handles requests to home page

    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST)  # create form with form data sent in request
        place = form.save(commit=False)  # create Place using form data but don't commit/save
        place.user = request.user  # relate the place to the logged-in user
        if form.is_valid():  # if user entered valid info - django automatically validates using DB constraints
            place.save()  # save the place to the DB
            return redirect('place_list')  # reload place_list

    # if not a POST method or form is invalid, load page with form to add new place and show list of places

    # make database query
    # filter and fetch unvisited Place objects from database and put into places list, sorted by name
    # also filters to show only the logged-in user's places
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')

    # create new place form
    new_place_form = NewPlaceForm()

    # renders/combines wishlist.html template, new place form, and list of Place objects to build webpage
    return render(request, 'travel_wishlist/wishlist.html',
                  {'places': places, 'new_place_form': new_place_form})


@login_required
def places_visited(request):  # handles requests to visited page

    # database query
    # filter and fetch visited Place objects from database and put into visited list
    # also filters to only show logged-in user's visited places
    visited = Place.objects.filter(user=request.user).filter(visited=True)

    return render(request, 'travel_wishlist/visited.html', {'visited': visited})


@login_required
def place_was_visited(request, place_pk):  # django extracts number from path to get place_pk

    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk)  # database query to get visited place matching the primary key
        place = get_object_or_404(Place, pk=place_pk)  # try to get object or return 404 error response
        if place.user == request.user:  # if user is marking their own place as visited
            place.visited = True  # can manipulate fields of model objects within views
            place.save()  # save DB
        else:
            return HttpResponseForbidden()

    #  return redirect('places_visited')  # redirect to places visited page
    return redirect('place_list')  # reload wishlist page


@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)  # try to get object or return 404 error response

    # is logged-in user the owner of the place?
    if place.user != request.user:
        return HttpResponseForbidden()

    # GET request (show data and form), or POST request (update Place object)?


    if request.method == 'POST':  # if POST, validate form and update Place object
        form = TripReviewForm(request.POST, request.FILES, instance=place)  # make form with data sent with request
        if form.is_valid():  # django validates using DB constraints
            form.save()  # save to DB
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors)

        return redirect('place_details', place_pk=place_pk)  # reload place details for this place

    else:  # if GET, show Place info and form
        # if place is visited, show form - no form if place is not visited
        if place.visited:
            review_form = TripReviewForm(instance=place)
            # combine html and data about single place to build page
            return render(request, 'travel_wishlist/place_detail.html', {'place': place,
                                                                         'review_form': review_form})
        else:  # don't include form
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})


@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)  # try to get object or return 404 error response
    if place.user == request.user:  # if user is trying to delete one of their places
        place.delete()  # delete from database
        return redirect('place_list')  # reload wishlist page
    else:  # if user is trying to delete a place that is not theirs
        return HttpResponseForbidden()


@login_required
def about(request):  # handles requests to about page
    author = 'Alexandrea'
    about = 'A website to create a list of places to visit'

    # combines about.html template with author and about data
    return render(request, 'travel_wishlist/about.html',
                  {'author': author, 'about': about})


