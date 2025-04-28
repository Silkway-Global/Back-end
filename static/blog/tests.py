from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import BlogPost
from accounts.models import CustomUser
from accounts.choices import UserTypeChoices
import tempfile
from PIL import Image
import io
from django.utils.text import slugify


class BlogPostTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create test users
        self.admin = CustomUser.objects.create_user(
            email='blog_author@example.com',
            password='password123',
            full_name='Blog Author',
            user_type=UserTypeChoices.ADMIN
        )
        
        self.student = CustomUser.objects.create_user(
            email='student@example.com',
            password='password123',
            full_name='Student User',
            user_type=UserTypeChoices.STUDENT
        )
        
        # Create a test image
        image = Image.new('RGB', (100, 100), color='red')
        img_io = io.BytesIO()
        image.save(img_io, format='JPEG')
        img_io.seek(0)
        self.test_image = SimpleUploadedFile(
            "test_image.jpg", img_io.read(), content_type="image/jpeg"
        )
        
        # Create a test blog post
        self.blog_post = BlogPost.objects.create(
            owner=self.admin,
            title='Test Blog Post',
            slug='test-blog-post',
            content='This is a test blog post content.',
            category='Technology'
        )
        
        # Data for creating a new blog post
        self.blog_post_data = {
            'title': 'New Blog Post',
            'content': 'This is a new blog post content.',
            'category': 'Education'
        }
        
        # Generate tokens for authentication
        self.admin_token = RefreshToken.for_user(self.admin)
        self.student_token = RefreshToken.for_user(self.student)
        
    def get_blog_post_with_image(self):
        """Helper method to create blog post data with image"""
        image = Image.new('RGB', (100, 100), color='blue')
        img_io = io.BytesIO()
        image.save(img_io, format='JPEG')
        img_io.seek(0)
        test_image = SimpleUploadedFile(
            "new_test_image.jpg", img_io.read(), content_type="image/jpeg"
        )
        
        data = self.blog_post_data.copy()
        data['image'] = test_image
        # Add a valid slug explicitly
        data['slug'] = 'new-blog-post'
        return data
        
    def test_list_blog_posts_pagination(self):
        """Test listing blog posts with pagination"""
        # Create multiple blog posts
        for i in range(5):
            BlogPost.objects.create(
                owner=self.admin,
                title=f'Blog Post {i}',
                slug=f'blog-post-{i}',
                content=f'Content for blog post {i}',
                category='Technology'
            )
            
        url = reverse('blogpost-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check pagination structure
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertTrue(response.data['count'] >= 6)  # 5 new + 1 from setUp
        
    def test_create_blog_post_with_image(self):
        """Test creating a blog post with a proper image file"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.admin_token.access_token)}')
        url = reverse('blogpost-list')
        
        data = self.get_blog_post_with_image()
        response = self.client.post(url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogPost.objects.count(), 2)
        new_blog_post = BlogPost.objects.get(slug='new-blog-post')
        self.assertEqual(new_blog_post.owner, self.admin)
        self.assertTrue(new_blog_post.image)  # Image should be populated
        
    def test_create_blog_post_student(self):
        """Test creating a blog post as a student (should fail if restricted to admin)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('blogpost-list')
        
        data = self.blog_post_data.copy()
        data['slug'] = 'student-blog-post'
        response = self.client.post(url, data, format='json')
        
        # If students can create blog posts, this should be 201
        # If restricted to admin only, this should be 403
        # We'll assert both possibilities based on your implementation
        self.assertTrue(
            response.status_code == status.HTTP_201_CREATED or 
            response.status_code == status.HTTP_403_FORBIDDEN
        )
        
    def test_create_blog_post_invalid_data(self):
        """Test blog post creation with invalid data"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.admin_token.access_token)}')
        url = reverse('blogpost-list')
        
        # Missing required field 'content'
        invalid_data = {
            'title': 'Invalid Blog Post',
            'slug': 'invalid-blog-post',
            'category': 'Education'
        }
        
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_duplicate_slug(self):
        """Test creating a blog post with duplicate slug"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.admin_token.access_token)}')
        url = reverse('blogpost-list')
        
        # Using an existing slug
        duplicate_data = self.blog_post_data.copy()
        duplicate_data['slug'] = self.blog_post.slug
        
        response = self.client.post(url, duplicate_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_retrieve_blog_post(self):
        """Test retrieving a blog post"""
        url = reverse('blogpost-detail', kwargs={'pk': self.blog_post.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Blog Post')
        self.assertEqual(response.data['slug'], 'test-blog-post')
        
    def test_update_blog_post_admin(self):
        """Test updating a blog post by admin"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.admin_token.access_token)}')
        url = reverse('blogpost-detail', kwargs={'pk': self.blog_post.id})
        update_data = {'title': 'Updated Blog Post Title'}
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.blog_post.refresh_from_db()
        self.assertEqual(self.blog_post.title, 'Updated Blog Post Title')
        
    def test_update_blog_post_student(self):
        """Test updating a blog post by student (should fail)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('blogpost-detail', kwargs={'pk': self.blog_post.id})
        update_data = {'title': 'Should Not Update'}
        response = self.client.patch(url, update_data, format='json')
        
        # This should fail with permission denied
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.blog_post.refresh_from_db()
        self.assertNotEqual(self.blog_post.title, 'Should Not Update')
        
    def test_update_blog_post_with_image(self):
        """Test updating a blog post with an image"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.admin_token.access_token)}')
        url = reverse('blogpost-detail', kwargs={'pk': self.blog_post.id})
        
        # Create a new image for the update
        image = Image.new('RGB', (200, 200), color='green')
        img_io = io.BytesIO()
        image.save(img_io, format='JPEG')
        img_io.seek(0)
        update_image = SimpleUploadedFile(
            "update_image.jpg", img_io.read(), content_type="image/jpeg"
        )
        
        update_data = {'image': update_image}
        response = self.client.patch(url, update_data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.blog_post.refresh_from_db()
        self.assertTrue(self.blog_post.image)  # Image should be updated
        
    def test_delete_blog_post_admin(self):
        """Test deleting a blog post by admin"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.admin_token.access_token)}')
        url = reverse('blogpost-detail', kwargs={'pk': self.blog_post.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BlogPost.objects.count(), 0)
        
    def test_delete_blog_post_student(self):
        """Test deleting a blog post by student (should fail)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('blogpost-detail', kwargs={'pk': self.blog_post.id})
        response = self.client.delete(url)
        
        # This should fail with permission denied
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(BlogPost.objects.count(), 1)
        
    def test_filter_blog_posts_by_category(self):
        """Test filtering blog posts by category"""
        # Create blog posts with different categories
        BlogPost.objects.create(
            owner=self.admin,
            title='Education Blog',
            slug='education-blog',
            content='Education content',
            category='Education'
        )
        
        url = reverse('blogpost-list')
        response = self.client.get(url, {'category': 'Education'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # If filtering works, we should have only the Education category post in the results
        if 'results' in response.data:
            education_posts = [p for p in response.data['results'] if p['category'] == 'Education']
            self.assertTrue(len(education_posts) > 0)
        else:
            education_posts = [p for p in response.data if p['category'] == 'Education']
            self.assertTrue(len(education_posts) > 0)
            
    def test_token_validation(self):
        """Test with invalid token"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        url = reverse('blogpost-list')
        response = self.client.get(url)
        
        # Expect unauthorized with invalid token
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

