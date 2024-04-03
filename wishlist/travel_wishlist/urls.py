from django.urls import path
from . import views

urlpatterns = [
    # represents a path to the home page
    # any request made to home page will be handled with place_list function in views module
    path('', views.place_list, name='place_list'),

    # path for visited page - requests are handled by places_visited function in views module
    path('visited', views.places_visited, name='places_visited'),

    # path for visiting a place - the primary key is included in the path so the place_was_visited
    # view knows which place was visited
    path('place/<int:place_pk>/was_visited/', views.place_was_visited, name='place_was_visited'),

    # path for a page about a single Place - uses primary key of place object so that place_details knows
    # which place to display
    path('place/<int:place_pk>', views.place_details, name='place_details'),

    # path for deleting a place - uses primary key in path so the delete_place function knows
    # which place to delete
    path('place/<int:place_pk>/delete', views.delete_place, name='delete_place'),

    # path for about page - requests are handled by about function in views module
    path('about', views.about, name='about')
]