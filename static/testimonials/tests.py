from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Testimonial
from accounts.models import CustomUser
from accounts.choices import UserTypeChoices


class TestimonialTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a test user
        self.user = CustomUser.objects.create_user(
            email='student@example.com',
            password='password123',
            full_name='Test Student',
            user_type=UserTypeChoices.STUDENT
        )
        
        # Create a test testimonial
        self.testimonial = Testimonial.objects.create(
            owner=self.user,
            university='Test University',
            story='This is my success story.',
            photo='test_photo.jpg',
            country='United Kingdom'
        )
        
        # Data for creating a new testimonial
        self.testimonial_data = {
            'university': 'New University',
            'story': 'This is a new success story.',
            'country': 'Australia',
            'photo': '',  # In real tests, use SimpleUploadedFile or mock
            'video_url': 'https://example.com/video'
        }
        
        # Authenticate client
        self.client.force_authenticate(user=self.user)
        
    def test_list_testimonials(self):
        url = reverse('testimonial-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
        
    def test_create_testimonial(self):
        url = reverse('testimonial-list')
        response = self.client.post(url, self.testimonial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Testimonial.objects.count(), 2)
        self.assertEqual(Testimonial.objects.get(university='New University').owner, self.user)
        
    def test_retrieve_testimonial(self):
        url = reverse('testimonial-detail', args=[self.testimonial.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['university'], 'Test University')
        
    def test_update_testimonial(self):
        url = reverse('testimonial-detail', args=[self.testimonial.id])
        update_data = {'university': 'Updated University Name'}
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.testimonial.refresh_from_db()
        self.assertEqual(self.testimonial.university, 'Updated University Name')
        
    def test_delete_testimonial(self):
        url = reverse('testimonial-detail', args=[self.testimonial.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Testimonial.objects.count(), 0)
        
    def test_unauthorized_testimonial_creation(self):
        # Create a new non-authenticated client
        unauthenticated_client = APIClient()
        url = reverse('testimonial-list')
        response = unauthenticated_client.post(url, self.testimonial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
