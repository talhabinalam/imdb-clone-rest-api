from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .models import *
from .serializers import *

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
            "website": "https://www.netflix.com",
        }
        response = self.client.post(reverse('stream-platform'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_stream_platform_list(self):
        response = self.client.get(reverse('stream-platform'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stream_platform_detail(self):
        response = self.client.get(reverse('stream-details', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)