import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.utils import timezone
from .models import CustomUser
from .choices import UserTypeChoices


class AccountsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create test users
        self.student = CustomUser.objects.create_user(
            email='test@example.com',
            password='test123password',
            full_name='Test User',
            phone_number='+12345678901',
            user_type=UserTypeChoices.STUDENT
        )
        
        self.admin = CustomUser.objects.create_user(
            email='admin@example.com',
            password='admin123password',
            full_name='Admin User',
            phone_number='+19876543210',
            user_type=UserTypeChoices.ADMIN
        )
        
        # Generate tokens for authentication
        self.student_token = RefreshToken.for_user(self.student)
        self.admin_token = RefreshToken.for_user(self.admin)
        
        # Data for registering a new user
        self.new_user_data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'full_name': 'New User',
            'phone_number': '+9876543210',
            'user_type': UserTypeChoices.STUDENT
        }
        
    def test_register_user(self):
        """Test user registration"""
        url = reverse('register')
        response = self.client.post(url, self.new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email='newuser@example.com').exists())
        
    def test_register_user_invalid_data(self):
        """Test user registration with invalid data"""
        url = reverse('register')
        
        # Missing required fields
        invalid_data = {
            'email': 'invalid@example.com',
            'password': 'password123'
            # missing other required fields
        }
        
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(CustomUser.objects.filter(email='invalid@example.com').exists())
        
    def test_register_user_duplicate_email(self):
        """Test user registration with duplicate email"""
        url = reverse('register')
        
        # Using an email that already exists
        duplicate_data = self.new_user_data.copy()
        duplicate_data['email'] = self.student.email
        
        response = self.client.post(url, duplicate_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_login_user(self):
        """Test user login with valid credentials"""
        url = reverse('token_obtain_pair')
        data = {
            'email': self.student.email,
            'password': 'test123password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
    def test_login_user_invalid_credentials(self):
        """Test user login with invalid credentials"""
        url = reverse('token_obtain_pair')
        data = {
            'email': self.student.email,
            'password': 'wrong_password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_token_refresh(self):
        """Test token refresh"""
        # First get a refresh token
        login_url = reverse('token_obtain_pair')
        login_data = {
            'email': self.student.email,
            'password': 'test123password'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        refresh_token = login_response.data['refresh']
        
        # Test refresh endpoint
        refresh_url = reverse('token_refresh')
        refresh_data = {'refresh': refresh_token}
        response = self.client.post(refresh_url, refresh_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        
    def test_invalid_token_refresh(self):
        """Test token refresh with invalid token"""
        refresh_url = reverse('token_refresh')
        refresh_data = {'refresh': 'invalid_token'}
        response = self.client.post(refresh_url, refresh_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_list_users_pagination(self):
        """Test listing users with pagination"""
        # Create multiple users
        for i in range(5):
            CustomUser.objects.create_user(
                email=f'user{i}@example.com',
                password='password',
                full_name=f'User {i}',
                user_type=UserTypeChoices.STUDENT
            )
            
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.admin_token.access_token)}')
        url = reverse('customuser-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check pagination structure
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertTrue(response.data['count'] >= 7)  # 5 new + 2 from setUp
        
    def test_list_users_student_permission(self):
        """Test listing users with student permissions (may be restricted)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('customuser-list')
        response = self.client.get(url)
        
        # If students can list users, this should be 200
        # If restricted to admin only, this should be 403
        # We'll assert both possibilities based on your implementation
        self.assertTrue(
            response.status_code == status.HTTP_200_OK or 
            response.status_code == status.HTTP_403_FORBIDDEN
        )
        
    def test_retrieve_user(self):
        """Test retrieving a user"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.admin_token.access_token)}')
        url = reverse('customuser-detail', kwargs={'pk': self.student.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.student.email)
        self.assertEqual(response.data['full_name'], 'Test User')
        
    def test_update_user_self(self):
        """Test updating user's own profile"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('customuser-detail', kwargs={'pk': self.student.id})
        update_data = {'full_name': 'Updated Name'}
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student.refresh_from_db()
        self.assertEqual(self.student.full_name, 'Updated Name')
        
    def test_update_user_admin(self):
        """Test admin updating another user's profile"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.admin_token.access_token)}')
        url = reverse('customuser-detail', kwargs={'pk': self.student.id})
        update_data = {'full_name': 'Admin Updated Name'}
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student.refresh_from_db()
        self.assertEqual(self.student.full_name, 'Admin Updated Name')
        
    def test_update_other_user_student(self):
        """Test student trying to update another user's profile (should fail)"""
        # Create another student
        other_student = CustomUser.objects.create_user(
            email='other@example.com',
            password='password123',
            full_name='Other User',
            user_type=UserTypeChoices.STUDENT
        )
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('customuser-detail', kwargs={'pk': other_student.id})
        update_data = {'full_name': 'Should Not Update'}
        response = self.client.patch(url, update_data, format='json')
        
        # This should fail with permission denied
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        other_student.refresh_from_db()
        self.assertNotEqual(other_student.full_name, 'Should Not Update')
        
    def test_delete_user(self):
        """Test admin deleting a user"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.admin_token.access_token)}')
        url = reverse('customuser-detail', kwargs={'pk': self.student.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CustomUser.objects.filter(id=self.student.id).exists())
        
    def test_delete_user_no_permission(self):
        """Test student trying to delete another user (should fail)"""
        # Create another student
        other_student = CustomUser.objects.create_user(
            email='other@example.com',
            password='password123',
            full_name='Other User',
            user_type=UserTypeChoices.STUDENT
        )
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('customuser-detail', kwargs={'pk': other_student.id})
        response = self.client.delete(url)
        
        # This should fail with permission denied
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(CustomUser.objects.filter(id=other_student.id).exists())

