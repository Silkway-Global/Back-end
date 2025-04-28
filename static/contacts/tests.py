from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import ContactMessage
from accounts.models import CustomUser
from accounts.choices import UserTypeChoices


class ContactMessageTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create test users
        self.student = CustomUser.objects.create_user(
            email='contact@example.com',
            password='password123',
            full_name='Contact User',
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
        
        # Create a test contact message
        self.contact_message = ContactMessage.objects.create(
            owner=self.student,
            subject='Information Request',
            message='I need more information about your services.'
        )
        
        # Data for creating a new contact message
        self.contact_message_data = {
            'subject': 'Admission Inquiry',
            'message': 'I am interested in applying for admission.'
        }
        
        # Generate tokens for authentication
        self.student_token = RefreshToken.for_user(self.student)
        self.other_student_token = RefreshToken.for_user(self.other_student)
        self.admin_token = RefreshToken.for_user(self.admin)
        
    def test_list_contact_messages_pagination(self):
        """Test listing contact messages with pagination"""
        # Create multiple contact messages
        for i in range(5):
            ContactMessage.objects.create(
                owner=self.student,
                subject=f'Subject {i}',
                message=f'Message content {i}'
            )
            
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('contactmessage-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check pagination structure
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertTrue(response.data['count'] >= 6)  # 5 new + 1 from setUp
        
    def test_create_contact_message(self):
        """Test creating a contact message"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('contactmessage-list')
        response = self.client.post(url, self.contact_message_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactMessage.objects.count(), 2)
        
        # Verify the message was created with correct data
        new_message = ContactMessage.objects.get(subject='Admission Inquiry')
        self.assertEqual(new_message.owner, self.student)
        self.assertEqual(new_message.message, 'I am interested in applying for admission.')
        
    def test_create_contact_message_invalid_data(self):
        """Test contact message creation with invalid data"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('contactmessage-list')
        
        # Missing required field 'message'
        invalid_data = {
            'subject': 'Subject Only'
            # missing message field
        }
        
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_retrieve_contact_message(self):
        """Test retrieving a contact message"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('contactmessage-detail', kwargs={'pk': self.contact_message.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['subject'], 'Information Request')
        self.assertEqual(response.data['message'], 'I need more information about your services.')
        
    def test_update_contact_message_owner(self):
        """Test updating a contact message by its owner"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('contactmessage-detail', kwargs={'pk': self.contact_message.id})
        update_data = {'subject': 'Updated Subject'}
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact_message.refresh_from_db()
        self.assertEqual(self.contact_message.subject, 'Updated Subject')
        
    def test_update_contact_message_other_user(self):
        """Test updating a contact message by a different user (should fail)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.other_student_token.access_token)}')
        url = reverse('contactmessage-detail', kwargs={'pk': self.contact_message.id})
        update_data = {'subject': 'Should Not Update'}
        response = self.client.patch(url, update_data, format='json')
        
        # This should fail with permission denied
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.contact_message.refresh_from_db()
        self.assertNotEqual(self.contact_message.subject, 'Should Not Update')
        
    def test_update_contact_message_admin(self):
        """Test updating a contact message by an admin user (should succeed)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.admin_token.access_token)}')
        url = reverse('contactmessage-detail', kwargs={'pk': self.contact_message.id})
        update_data = {'subject': 'Admin Updated'}
        response = self.client.patch(url, update_data, format='json')
        
        # Admin should be able to update
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact_message.refresh_from_db()
        self.assertEqual(self.contact_message.subject, 'Admin Updated')
        
    def test_delete_contact_message_owner(self):
        """Test deleting a contact message by its owner"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('contactmessage-detail', kwargs={'pk': self.contact_message.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ContactMessage.objects.count(), 0)
        
    def test_delete_contact_message_other_user(self):
        """Test deleting a contact message by a different user (should fail)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.other_student_token.access_token)}')
        url = reverse('contactmessage-detail', kwargs={'pk': self.contact_message.id})
        response = self.client.delete(url)
        
        # This should fail with permission denied
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(ContactMessage.objects.count(), 1)
        
    def test_multiple_contact_messages_per_user(self):
        """Test creating multiple contact messages per user (should succeed)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(self.student_token.access_token)}')
        url = reverse('contactmessage-list')
        
        # Create multiple messages for the same user
        for i in range(3):
            data = {
                'subject': f'Multiple Subject {i}',
                'message': f'Multiple message content {i}'
            }
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            
        # Verify the user has multiple messages
        self.assertEqual(ContactMessage.objects.filter(owner=self.student).count(), 4)  # 3 new + 1 from setUp
        
    def test_token_validation(self):
        """Test with invalid token"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        url = reverse('contactmessage-list')
        response = self.client.get(url)
        
        # Expect unauthorized with invalid token
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_anonymous_user_view_messages(self):
        """Test if anonymous users can view contact messages (should fail)"""
        url = reverse('contactmessage-list')
        response = self.client.get(url)
        
        # Anonymous users should not have access
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
