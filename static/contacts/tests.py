from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import ContactMessage
from accounts.models import CustomUser
from accounts.choices import UserTypeChoices


class ContactMessageTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a test user
        self.user = CustomUser.objects.create_user(
            email='contact@example.com',
            password='password123',
            full_name='Contact User',
            user_type=UserTypeChoices.STUDENT
        )
        
        # Create a test contact message
        self.contact_message = ContactMessage.objects.create(
            owner=self.user,
            subject='Information Request',
            message='I need more information about your services.'
        )
        
        # Data for creating a new contact message
        self.contact_message_data = {
            'subject': 'Admission Inquiry',
            'message': 'I am interested in applying for admission.'
        }
        
        # Authenticate client
        self.client.force_authenticate(user=self.user)
        
    def test_list_contact_messages(self):
        url = reverse('contactmessage-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
        
    def test_create_contact_message(self):
        url = reverse('contactmessage-list')
        response = self.client.post(url, self.contact_message_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactMessage.objects.count(), 2)
        self.assertEqual(ContactMessage.objects.get(subject='Admission Inquiry').owner, self.user)
        
    def test_retrieve_contact_message(self):
        url = reverse('contactmessage-detail', args=[self.contact_message.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['subject'], 'Information Request')
        
    def test_update_contact_message(self):
        url = reverse('contactmessage-detail', args=[self.contact_message.id])
        update_data = {'subject': 'Updated Subject'}
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact_message.refresh_from_db()
        self.assertEqual(self.contact_message.subject, 'Updated Subject')
        
    def test_delete_contact_message(self):
        url = reverse('contactmessage-detail', args=[self.contact_message.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ContactMessage.objects.count(), 0)
        
    def test_unauthorized_contact_message_creation(self):
        # Create a new non-authenticated client
        unauthenticated_client = APIClient()
        url = reverse('contactmessage-list')
        response = unauthenticated_client.post(url, self.contact_message_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
