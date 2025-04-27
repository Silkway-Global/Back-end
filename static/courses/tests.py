from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Course
from accounts.models import CustomUser
from accounts.choices import UserTypeChoices
from decimal import Decimal
import datetime


class CourseTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a test user
        self.user = CustomUser.objects.create_user(
            email='course_owner@example.com',
            password='password123',
            full_name='Course Owner',
            user_type=UserTypeChoices.ADMIN
        )
        
        # Create a test course
        self.course = Course.objects.create(
            owner=self.user,
            title='Test Course',
            description='Test course description',
            duration_weeks=8,
            price=Decimal('199.99'),
            country='United States',
            category='Programming',
            start_date=datetime.date.today() + datetime.timedelta(days=30),
            image='test_image.jpg'
        )
        
        # Data for creating a new course
        self.course_data = {
            'title': 'New Course',
            'description': 'New course description',
            'duration_weeks': 12,
            'price': '299.99',
            'country': 'Canada',
            'category': 'Data Science',
            'start_date': (datetime.date.today() + datetime.timedelta(days=60)).isoformat(),
            'image': ''  # In real tests, use SimpleUploadedFile or mock
        }
        
        # Authenticate client
        self.client.force_authenticate(user=self.user)
        
    def test_list_courses(self):
        url = reverse('course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
        
    def test_create_course(self):
        url = reverse('course-list')
        response = self.client.post(url, self.course_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(Course.objects.get(title='New Course').owner, self.user)
        
    def test_retrieve_course(self):
        url = reverse('course-detail', args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Course')
        
    def test_update_course(self):
        url = reverse('course-detail', args=[self.course.id])
        update_data = {'title': 'Updated Course Title'}
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, 'Updated Course Title')
        
    def test_delete_course(self):
        url = reverse('course-detail', args=[self.course.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)
        
    def test_unauthorized_course_creation(self):
        # Create a new non-authenticated client
        unauthenticated_client = APIClient()
        url = reverse('course-list')
        response = unauthenticated_client.post(url, self.course_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
