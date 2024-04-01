from django.test import TestCase
from django.urls import reverse

from .models import Place


class TestHomePage(TestCase):

    def test_home_page_shows_empty_list_for_empty_database(self):
        home_page_url = reverse('place_list')  # plan request
        response = self.client.get(home_page_url)  # make request

        # make assertions about response
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'You have no places in your wishlist.')


class TestWishList(TestCase):

    fixtures = ['test_places']  # load in fixtures

    def test_wishlist_contains_not_visited_places(self):
        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'New York')
        self.assertNotContains(response, 'San Francisco')
        self.assertNotContains(response, 'Moab')


class TestVisitedPage(TestCase):

    def test_visited_page_shows_empty_list_message_for_empty_database(self):
        response = self.client.get(reverse('places_visited'))  # make request

        # make assertions about response
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'You have not visited any places yet')


class VisitedList(TestCase):

    fixtures = ['test_places']

    def test_visited_list_contains_visited_places(self):
        response = self.client.get(reverse('places_visited'))

        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'San Francisco')
        self.assertContains(response, 'Moab')
        self.assertNotContains(response, 'New York')
        self.assertNotContains(response, 'Tokyo')


class TestAddNewPlace(TestCase):

    def test_add_new_unvisited_place(self):
        add_place_url = reverse('place_list')
        new_place_data = {'name': 'Tokyo', 'visited': False}  # create example place to add

        response = self.client.post(add_place_url, new_place_data, follow=True)  # make post request

        # make assertions about response
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        response_places = response.context['places']
        self.assertEqual(1, len(response_places))  # test that there is only one place
        tokyo_from_response = response_places[0]

        tokyo_from_database = Place.objects.get(name='Tokyo', visited=False)  # query database
        self.assertEqual(tokyo_from_database, tokyo_from_response)  # assert response matches database


class TestVisitPlace(TestCase):

    fixtures = ['test_places']

    def test_visit_place(self):

        # pk number 2 = New York
        visit_place_url = reverse('place_was_visited', args=(2, ))  # build URL that makes pk 2 a visited place
        response = self.client.post(visit_place_url, follow=True)

        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        self.assertNotContains(response, 'New York')  # NY should not be in place list anymore
        self.assertContains(response, 'Tokyo')  # Tokyo should still be there, was not visited

        new_york_database = Place.objects.get(pk=2)
        self.assertTrue(new_york_database.visited)  # assert that new york is True for visited field in DB

    def test_non_existent_place(self):
        # url to visit a place that does not exist
        visit_non_existing_place_url = reverse('place_was_visited', args=(123456, ))
        response = self.client.post(visit_non_existing_place_url, follow=True)

        self.assertEqual(404, response.status_code)  # assert 404 error response
