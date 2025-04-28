from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Appointment
from accounts.models import CustomUser
from accounts.choices import UserTypeChoices
import datetime


class AppointmentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create test users
        self.student = CustomUser.objects.create_user(
            email='student@example.com',
            password='password123',
            full_name='Test Student',
            user_type=UserTypeChoices.STUDENT
        )
        
        self.other_student = CustomUser.objects.create_user(
            email='other_student@example.com',
            password='password123',
            full_name='Other Student',
            user_type=UserTypeChoices.STUDENT
        )
        
        self.admin = CustomUser.objects.create_user(
            email='admin@example.com',
            password='password123',
            full_name='Admin User',
            user_type=UserTypeChoices.ADMIN
        )
        
        # Create a test appointment with proper date objects
        self.appointment_date = datetime.date.today() + datetime.timedelta(days=7)
        self.appointment_time = datetime.time(14, 0)
        
        self.appointment = Appointment.objects.create(
            owner=self.student,
            preferred_date=self.appointment_date,
            preferred_time=self.appointment_time,
            message='I would like to discuss admission requirements.'
        )
        
        # Data for creating a new appointment - use ISO format for date/time
        future_date = datetime.date.today() + datetime.timedelta(days=14)
        self.appointment_data = {
            'preferred_date': future_date.isoformat(),
            'preferred_time': '15:30:00',
            'message': 'I would like to discuss scholarship opportunities.'
        }
        
        # Generate tokens for authentication
        self.student_token = RefreshToken.for_user(self.student)
        self.other_student_token = RefreshToken.for_user(self.other_student)
        self.admin_token = RefreshToken.for_user(self.admin)
        
    def test_list_appointments_pagination(self):
        """Test listing appointments with pagination"""
        # Create multiple appointments
        for i in range(5):
            future_date = datetime.date.today() + datetime.timedelta(days=i+1)
            Appointment.objects.create(
                owner=self.student,
                preferred_date=future_date,
                preferred_time=datetime.time(10, 0),
                message=f'Appointment request {i}'
            )
            
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('appointment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check pagination structure
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertTrue(response.data['count'] >= 6)  # 5 new + 1 from setUp
        
    def test_create_appointment(self):
        """Test creating an appointment"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('appointment-list')
        response = self.client.post(url, self.appointment_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 2)
        
        # Verify the appointment was created with correct data
        new_appointment = Appointment.objects.get(message='I would like to discuss scholarship opportunities.')
        self.assertEqual(new_appointment.owner, self.student)
        self.assertEqual(new_appointment.preferred_time.strftime('%H:%M:%S'), '15:30:00')
        
    def test_create_appointment_invalid_date(self):
        """Test creating an appointment with invalid date"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('appointment-list')
        
        # Past date (invalid)
        past_date = datetime.date.today() - datetime.timedelta(days=1)
        invalid_data = self.appointment_data.copy()
        invalid_data['preferred_date'] = past_date.isoformat()
        
        response = self.client.post(url, invalid_data, format='json')
        # Should fail validation
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_appointment_invalid_time(self):
        """Test creating an appointment with invalid time format"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('appointment-list')
        
        # Invalid time format
        invalid_data = self.appointment_data.copy()
        invalid_data['preferred_time'] = 'not a time'
        
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_retrieve_appointment(self):
        """Test retrieving an appointment"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('appointment-detail', kwargs={'pk': self.appointment.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'I would like to discuss admission requirements.')
        
        # Check date and time format in response
        self.assertEqual(response.data['preferred_date'], self.appointment_date.isoformat())
        self.assertEqual(response.data['preferred_time'], self.appointment_time.strftime('%H:%M:%S'))
        
    def test_update_appointment_owner(self):
        """Test updating an appointment by its owner"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('appointment-detail', kwargs={'pk': self.appointment.id})
        
        # Update time
        new_time = '16:00:00'
        update_data = {'preferred_time': new_time}
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.preferred_time.strftime('%H:%M:%S'), new_time)
        
    def test_update_appointment_other_user(self):
        """Test updating an appointment by a different user (should fail)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.other_student_token.access_token)}')
        url = reverse('appointment-detail', kwargs={'pk': self.appointment.id})
        update_data = {'preferred_time': '17:00:00'}
        response = self.client.patch(url, update_data, format='json')
        
        # Should fail with permission denied
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.appointment.refresh_from_db()
        self.assertNotEqual(self.appointment.preferred_time.strftime('%H:%M:%S'), '17:00:00')
        
    def test_update_appointment_admin(self):
        """Test updating an appointment by an admin user (should succeed)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.admin_token.access_token)}')
        url = reverse('appointment-detail', kwargs={'pk': self.appointment.id})
        new_time = '18:00:00'
        update_data = {'preferred_time': new_time}
        response = self.client.patch(url, update_data, format='json')
        
        # Admin should be able to update
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.preferred_time.strftime('%H:%M:%S'), new_time)
        
    def test_delete_appointment_owner(self):
        """Test deleting an appointment by its owner"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('appointment-detail', kwargs={'pk': self.appointment.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Appointment.objects.count(), 0)
        
    def test_delete_appointment_other_user(self):
        """Test deleting an appointment by a different user (should fail)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.other_student_token.access_token)}')
        url = reverse('appointment-detail', kwargs={'pk': self.appointment.id})
        response = self.client.delete(url)
        
        # Should fail with permission denied
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Appointment.objects.count(), 1)
        
    def test_multiple_appointments_per_user(self):
        """Test creating multiple appointments per user (should succeed)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('appointment-list')
        
        # Create multiple appointments for the same user
        for i in range(3):
            future_date = datetime.date.today() + datetime.timedelta(days=i+10)
            data = {
                'preferred_date': future_date.isoformat(),
                'preferred_time': f'{10+i}:00:00',
                'message': f'Appointment request {i}'
            }
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            
        # Verify the user has multiple appointments
        self.assertEqual(Appointment.objects.filter(owner=self.student).count(), 4)  # 3 new + 1 from setUp
        
    def test_token_validation(self):
        """Test with invalid token"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        url = reverse('appointment-list')
        response = self.client.get(url)
        
        # Expect unauthorized with invalid token
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_expired_token(self):
        """Test with expired token (simulate by using a made-up token)"""
        # This is a simplified simulation - in reality we would need to create an expired token
        expired_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE2MjM5MDIyLCJqdGkiOiJmODk0YzMzNDMxZTc0OGQ2ODJjZmYxYTQ0YWRlZGJlZiIsInVzZXJfaWQiOjF9.mUHXRWzRn_lNbHJR45D9C7mS0M-2AlLU7E6IwsW5GaM"
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {expired_token}')
        url = reverse('appointment-list')
        response = self.client.get(url)
        
        # Expect unauthorized with expired token
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

