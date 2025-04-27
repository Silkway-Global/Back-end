from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Appointment
from accounts.models import CustomUser
from accounts.choices import UserTypeChoices
import datetime


class AppointmentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a test user
        self.user = CustomUser.objects.create_user(
            email='student@example.com',
            password='password123',
            full_name='Test Student',
            user_type=UserTypeChoices.STUDENT
        )
        
        # Create a test appointment
        self.appointment = Appointment.objects.create(
            owner=self.user,
            preferred_date=datetime.date.today() + datetime.timedelta(days=7),
            preferred_time=datetime.time(14, 0),
            message='I would like to discuss admission requirements.'
        )
        
        # Data for creating a new appointment
        self.appointment_data = {
            'preferred_date': (datetime.date.today() + datetime.timedelta(days=14)).isoformat(),
            'preferred_time': '15:30:00',
            'message': 'I would like to discuss scholarship opportunities.'
        }
        
        # Authenticate client
        self.client.force_authenticate(user=self.user)
        
    def test_list_appointments(self):
        url = reverse('appointment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
        
    def test_create_appointment(self):
        url = reverse('appointment-list')
        response = self.client.post(url, self.appointment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 2)
        self.assertEqual(Appointment.objects.get(message='I would like to discuss scholarship opportunities.').owner, self.user)
        
    def test_retrieve_appointment(self):
        url = reverse('appointment-detail', args=[self.appointment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'I would like to discuss admission requirements.')
        
    def test_update_appointment(self):
        url = reverse('appointment-detail', args=[self.appointment.id])
        update_data = {'preferred_time': '16:00:00'}
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.preferred_time.strftime('%H:%M:%S'), '16:00:00')
        
    def test_delete_appointment(self):
        url = reverse('appointment-detail', args=[self.appointment.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Appointment.objects.count(), 0)
        
    def test_unauthorized_appointment_creation(self):
        # Create a new non-authenticated client
        unauthenticated_client = APIClient()
        url = reverse('appointment-list')
        response = unauthenticated_client.post(url, self.appointment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

