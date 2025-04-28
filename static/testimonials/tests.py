from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Testimonial
from accounts.models import CustomUser
from accounts.choices import UserTypeChoices
import tempfile
from PIL import Image
import io


class TestimonialTests(TestCase):
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
        
        # Create a test image
        image = Image.new('RGB', (100, 100), color='red')
        img_io = io.BytesIO()
        image.save(img_io, format='JPEG')
        img_io.seek(0)
        self.test_image = SimpleUploadedFile(
            "test_image.jpg", img_io.read(), content_type="image/jpeg"
        )
        
        # Create a test testimonial
        self.testimonial = Testimonial.objects.create(
            owner=self.student,
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
            'video_url': 'https://example.com/video'
        }
        
        # Generate tokens for authentication
        self.student_token = RefreshToken.for_user(self.student)
        self.other_student_token = RefreshToken.for_user(self.other_student)
        self.admin_token = RefreshToken.for_user(self.admin)
        
    def get_testimonial_with_image(self):
        """Helper method to create testimonial data with image"""
        image = Image.new('RGB', (100, 100), color='blue')
        img_io = io.BytesIO()
        image.save(img_io, format='JPEG')
        img_io.seek(0)
        test_image = SimpleUploadedFile(
            "new_test_image.jpg", img_io.read(), content_type="image/jpeg"
        )
        
        data = self.testimonial_data.copy()
        data['photo'] = test_image
        return data
        
    def test_list_testimonials_pagination(self):
        """Test listing testimonials with pagination"""
        # Create multiple testimonials
        for i in range(5):
            Testimonial.objects.create(
                owner=self.student,
                university=f'University {i}',
                story=f'Success story {i}',
                country='Country'
            )
            
        url = reverse('testimonial-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check pagination structure
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertTrue(response.data['count'] >= 6)  # 5 new + 1 from setUp
        
    def test_create_testimonial_with_image(self):
        """Test creating a testimonial with a proper image file"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.other_student_token.access_token)}')
        url = reverse('testimonial-list')
        
        data = self.get_testimonial_with_image()
        response = self.client.post(url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Testimonial.objects.count(), 2)
        new_testimonial = Testimonial.objects.get(university='New University')
        self.assertEqual(new_testimonial.owner, self.other_student)
        self.assertTrue(new_testimonial.photo)  # Photo should be populated
        
    def test_create_testimonial_invalid_data(self):
        """Test testimonial creation with invalid data"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('testimonial-list')
        
        # Missing required field 'story'
        invalid_data = {
            'university': 'New University',
            'country': 'Australia'
        }
        
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_retrieve_testimonial(self):
        """Test retrieving a testimonial"""
        url = reverse('testimonial-detail', kwargs={'pk': self.testimonial.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['university'], 'Test University')
        
    def test_update_testimonial_owner(self):
        """Test updating a testimonial by its owner"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('testimonial-detail', kwargs={'pk': self.testimonial.id})
        update_data = {'university': 'Updated University Name'}
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Get fresh data from database to verify update
        updated_testimonial = Testimonial.objects.get(pk=self.testimonial.id)
        self.assertEqual(updated_testimonial.university, 'Updated University Name')
        
    def test_update_testimonial_other_user(self):
        """Test updating a testimonial by a different user (should fail)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.other_student_token.access_token)}')
        url = reverse('testimonial-detail', kwargs={'pk': self.testimonial.id})
        update_data = {'university': 'Should Not Update'}
        response = self.client.patch(url, update_data, format='json')
        
        # This should fail with permission denied
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.testimonial.refresh_from_db()
        self.assertNotEqual(self.testimonial.university, 'Should Not Update')
        
    def test_update_testimonial_admin(self):
        """Test updating a testimonial by an admin user (should succeed)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.admin_token.access_token)}')
        url = reverse('testimonial-detail', kwargs={'pk': self.testimonial.id})
        update_data = {'university': 'Admin Updated'}
        response = self.client.patch(url, update_data, format='json')
        
        # Admin should be able to update
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Get fresh data from database to verify update
        updated_testimonial = Testimonial.objects.get(pk=self.testimonial.id)
        self.assertEqual(updated_testimonial.university, 'Admin Updated')
        
    def test_delete_testimonial_owner(self):
        """Test deleting a testimonial by its owner"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('testimonial-detail', kwargs={'pk': self.testimonial.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Testimonial.objects.count(), 0)
        
    def test_delete_testimonial_other_user(self):
        """Test deleting a testimonial by a different user (should fail)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.other_student_token.access_token)}')
        url = reverse('testimonial-detail', kwargs={'pk': self.testimonial.id})
        response = self.client.delete(url)
        
        # This should fail with permission denied
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Testimonial.objects.count(), 1)
        
    def test_create_duplicate_testimonial(self):
        """Test creating a duplicate testimonial (assume one per user)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('testimonial-list')
        
        # Student already has a testimonial
        data = self.get_testimonial_with_image()
        response = self.client.post(url, data, format='multipart')
        
        # If your model enforces unique constraints (e.g., one testimonial per user)
        # Expect this to fail with a 400 error
        if Testimonial._meta.unique_together and ('owner',) in Testimonial._meta.unique_together:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(Testimonial.objects.count(), 1)
        else:
            # If no uniqueness constraint, it should succeed
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_token_validation(self):
        """Test with invalid token"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        url = reverse('testimonial-list')
        response = self.client.get(url)
        
        # Expect unauthorized with invalid token
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
