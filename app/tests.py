from select import select

from .models import *

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = StreamPlatform.objects.create(name="Netflix", about="Streaming Platform",
                                                        website="https://www.netflix.com",)

    def test_create_stream_platform(self):
        data = {
            "name": "Netflix",
            "about": "Streaming Platform",
            "website": "https://www.netflix.com"
        }
        response = self.client.post(reverse('stream-platform'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_stream_platform_list(self):
        response = self.client.get(reverse('stream-platform'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stream_platform_detail(self):
        response = self.client.get(reverse('stream-details', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WatchlistTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='example', password='password@123')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = StreamPlatform.objects.create(name="Netflix", about="Streaming Platform",
                                                        website="https://www.netflix.com")
        self.watchlist = WatchList.objects.create(platform=self.stream, title="Spider Man",
                                                  description="Movie", active=True)

    def test_create_watchlist(self):
        data = {
            "title": "Spider Man",
            "description": "Movie",
            "platform": self.stream.id,
            "active": True
        }

        response = self.client.post(reverse('watchlist'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response = self.client.get(reverse('watchlist'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_detail(self):
        response = self.client.get(reverse('watchlist-details', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(WatchList.objects.count(), 1)
        self.assertEqual(WatchList.objects.get().title, 'Spider Man')


class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='example', password='password@123')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = StreamPlatform.objects.create(name="Netflix", about="Streaming Platform",
                                                    website="https://www.netflix.com")
        self.watchlist = WatchList.objects.create(platform=self.stream, title="Spider Man",
                                                  description="Movie", active=True)
        self.watchlist2 = WatchList.objects.create(platform=self.stream, title="Spider Man",
                                                  description="Movie", active=True)

        self.review = Review.objects.create(review_user=self.user, rating=5, description="Review",
                                            watchlist=self.watchlist2, active=True)

    def test_review_create(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "Good movie!",
            "watchlist": self.watchlist.id,
            "active": True
        }

        response = self.client.post(reverse('review-create', args=[self.watchlist.id]), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)
        # self.assertEqual(Review.objects.get().rating, 5)

        response = self.client.post(reverse('review-create', args=[self.watchlist.id]), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_create_unath(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "Good movie!",
            "watchlist": self.watchlist.id,
            "active": True
        }

        self.client.force_authenticate(user=None) # Logging out authenticated user!
        response = self.client.post(reverse('review-create', args=[self.watchlist.id]), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            "review_user": self.user,
            "rating": 4,
            "description": "Good movie! - Updated",
            "watchlist": self.watchlist.id,
            "active": True
        }
        response = self.client.put(reverse('review-detail', args=[self.review.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reviewlist(self):
        response = self.client.get(reverse('review-list', args=[self.watchlist.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_detail(self):
        response = self.client.get(reverse('review-detail', args=[self.review.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_delete(self):
        response = self.client.delete(reverse('review-detail', args=[self.review.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_review_user(self):
        response = self.client.get('/api/reviews/?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
