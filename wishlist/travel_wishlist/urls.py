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

    # path for about page - requests are handled by about function in views module
    path('about', views.about, name='about')
]