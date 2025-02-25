from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from planetarium.models import (
    AstronomyShow, ShowTheme, PlanetariumDome, ShowSession, Reservation
)

User = get_user_model()

class BaseViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="testpass")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


class AstronomyShowViewSetTest(BaseViewSetTest):
    def setUp(self):
        super().setUp()
        self.show = AstronomyShow.objects.create(title="Test Show", description="Test Description")
        self.url = "/api/planetarium/astronomy-shows/"

    def test_list_shows(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_show(self):
        data = {"title": "New Show", "description": "New Description"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ShowThemeViewSetTest(BaseViewSetTest):
    def setUp(self):
        super().setUp()
        self.theme = ShowTheme.objects.create(name="Space")
        self.url = "/api/planetarium/show-themes/"

    def test_list_themes(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PlanetariumDomeViewSetTest(BaseViewSetTest):
    def setUp(self):
        super().setUp()
        self.dome = PlanetariumDome.objects.create(name="Main Dome", rows=10, seats_in_row=20)
        self.url = "/api/planetarium/planetarium-domes/"

    def test_list_domes(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ShowSessionViewSetTest(BaseViewSetTest):
    def setUp(self):
        super().setUp()
        self.show = AstronomyShow.objects.create(title="Galaxy Show", description="Test")
        self.dome = PlanetariumDome.objects.create(name="Dome 1", rows=5, seats_in_row=10)
        self.session = ShowSession.objects.create(
            astronomy_show=self.show,
            planetarium_dome=self.dome,
            show_time="2025-02-25T10:00:00Z"
        )
        self.url = "/api/planetarium/show-sessions/"

    def test_list_sessions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ReservationViewSetTest(BaseViewSetTest):
    def setUp(self):
        super().setUp()
        self.show = AstronomyShow.objects.create(title="Galaxy Show", description="Test")
        self.dome = PlanetariumDome.objects.create(name="Dome 1", rows=5, seats_in_row=10)
        self.session = ShowSession.objects.create(
            astronomy_show=self.show,
            planetarium_dome=self.dome,
            show_time="2025-02-25T10:00:00Z"
        )
        self.url = reverse('planetarium:reservation-list')

    def test_create_reservation(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "tickets": [  # Provide at least one ticket
                {
                    "show_session": self.session.id,
                    "seat": 1,
                    "row": 1,
                    "reservation": 1
                }
            ]
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
