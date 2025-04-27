from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import BlogPost
from accounts.models import CustomUser
from accounts.choices import UserTypeChoices


class BlogPostTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a test user
        self.user = CustomUser.objects.create_user(
            email='blog_author@example.com',
            password='password123',
            full_name='Blog Author',
            user_type=UserTypeChoices.ADMIN
        )
        
        # Create a test blog post
        self.blog_post = BlogPost.objects.create(
            owner=self.user,
            title='Test Blog Post',
            slug='test-blog-post',
            content='This is a test blog post content.',
            category='Technology'
        )
        
        # Data for creating a new blog post
        self.blog_post_data = {
            'title': 'New Blog Post',
            'slug': 'new-blog-post',
            'content': 'This is a new blog post content.',
            'category': 'Education',
            'image': ''  # In real tests, use SimpleUploadedFile or mock
        }
        
        # Authenticate client
        self.client.force_authenticate(user=self.user)
        
    def test_list_blog_posts(self):
        url = reverse('blogpost-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
        
    def test_create_blog_post(self):
        url = reverse('blogpost-list')
        response = self.client.post(url, self.blog_post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BlogPost.objects.count(), 2)
        self.assertEqual(BlogPost.objects.get(slug='new-blog-post').owner, self.user)
        
    def test_retrieve_blog_post(self):
        url = reverse('blogpost-detail', args=[self.blog_post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Blog Post')
        
    def test_update_blog_post(self):
        url = reverse('blogpost-detail', args=[self.blog_post.id])
        update_data = {'title': 'Updated Blog Post Title'}
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.blog_post.refresh_from_db()
        self.assertEqual(self.blog_post.title, 'Updated Blog Post Title')
        
    def test_delete_blog_post(self):
        url = reverse('blogpost-detail', args=[self.blog_post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BlogPost.objects.count(), 0)
        
    def test_unauthorized_blog_post_creation(self):
        # Create a new non-authenticated client
        unauthenticated_client = APIClient()
        url = reverse('blogpost-list')
        response = unauthenticated_client.post(url, self.blog_post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

