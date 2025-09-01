from django.test import TestCase, RequestFactory
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from unittest.mock import patch, MagicMock
from .views import index, autocomplete, buy, barter, feedback_view, inbox_view
from .forms import CropSearchForm, Compare, FeedbackForm
from .models import Feedback


class IndexViewTest(TestCase):
    
    def test_index_view(self):
        """Test that index view returns correct response"""
        # Create a request
        request = RequestFactory().get('/')
        
        # Call the view
        response = index(request)
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'main/index.html')


class AutocompleteViewTest(TestCase):
    
    @patch('main.views.get_matching_crops')
    def test_autocomplete_view(self, mock_get_matching_crops):
        """Test autocomplete view with valid term"""
        # Mock the return value
        mock_get_matching_crops.return_value = ['APPLE - CARTON', 'APPLE - BOX']
        
        # Create a request with term parameter
        request = RequestFactory().get('/autocomplete/', {'term': 'apple'})
        
        # Call the view
        response = autocomplete(request)
        
        # Check response
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'["APPLE - CARTON", "APPLE - BOX"]')
        
        # Verify function was called with uppercase term
        mock_get_matching_crops.assert_called_once_with('APPLE')
    
    @patch('main.views.get_matching_crops')
    def test_autocomplete_view_empty_term(self, mock_get_matching_crops):
        """Test autocomplete view with empty term"""
        # Mock the return value
        mock_get_matching_crops.return_value = []
        
        # Create a request with empty term
        request = RequestFactory().get('/autocomplete/', {'term': ''})
        
        # Call the view
        response = autocomplete(request)
        
        # Check response
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'[]')
        
        # Verify function was called with empty string
        mock_get_matching_crops.assert_called_once_with('')
    
    def test_autocomplete_view_require_get(self):
        """Test that autocomplete view only accepts GET requests"""
        # Try to make a POST request
        request = RequestFactory().post('/autocomplete/')
        
        # Should raise an error or return 405
        with self.assertRaises(Exception):
            autocomplete(request)


class BuyViewTest(TestCase):
    
    @patch('main.views.priceOf')
    def test_buy_view_get(self, mock_priceOf):
        """Test buy view with GET request"""
        # Create a GET request
        request = RequestFactory().get('/buy/')
        
        # Call the view
        response = buy(request)
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'main/buy.html')
        
        # Check that form is in context
        self.assertIn('form', response.context_data)
        self.assertIsInstance(response.context_data['form'], CropSearchForm)
        
        # Check that result is None for GET requests
        self.assertIsNone(response.context_data['result'])
        
        # priceOf should not be called for GET requests
        mock_priceOf.assert_not_called()
    
    @patch('main.views.priceOf')
    def test_buy_view_post_valid(self, mock_priceOf):
        """Test buy view with valid POST request"""
        # Mock the priceOf function
        mock_priceOf.return_value = '5.50'
        
        # Create a POST request with valid data
        request = RequestFactory().post('/buy/', {'crop': 'APPLE - CARTON'})
        
        # Call the view
        response = buy(request)
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'main/buy.html')
        
        # Check that form is in context
        self.assertIn('form', response.context_data)
        
        # Check that result is set correctly
        self.assertEqual(response.context_data['result'], ['APPLE - CARTON', '5.50'])
        
        # Verify priceOf was called with uppercase crop name
        mock_priceOf.assert_called_once_with('APPLE - CARTON')
    
    @patch('main.views.priceOf')
    def test_buy_view_post_invalid(self, mock_priceOf):
        """Test buy view with invalid POST request"""
        # Create a POST request with invalid data (empty crop)
        request = RequestFactory().post('/buy/', {'crop': ''})
        
        # Call the view
        response = buy(request)
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'main/buy.html')
        
        # Check that form is in context and has errors
        self.assertIn('form', response.context_data)
        self.assertFalse(response.context_data['form'].is_valid())
        
        # Check that result is None for invalid forms
        self.assertIsNone(response.context_data['result'])
        
        # priceOf should not be called for invalid forms
        mock_priceOf.assert_not_called()


class BarterViewTest(TestCase):
    
    @patch('main.views.compare')
    def test_barter_view_get(self, mock_compare):
        """Test barter view with GET request"""
        # Create a GET request
        request = RequestFactory().get('/barter/')
        
        # Call the view
        response = barter(request)
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'main/barter.html')
        
        # Check that form is in context
        self.assertIn('form', response.context_data)
        self.assertIsInstance(response.context_data['form'], Compare)
        
        # Check that result is None for GET requests
        self.assertIsNone(response.context_data['result'])
        
        # compare should not be called for GET requests
        mock_compare.assert_not_called()
    
    @patch('main.views.compare')
    def test_barter_view_post_valid(self, mock_compare):
        """Test barter view with valid POST request"""
        # Mock the compare function
        mock_compare.return_value = ('APPLE', '1.5', 'ORANGE', '0.67', '5.50', '8.25')
        
        # Create a POST request with valid data
        request = RequestFactory().post('/barter/', {
            'crop1': 'APPLE - CARTON',
            'crop2': 'ORANGE - BOX'
        })
        
        # Call the view
        response = barter(request)
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'main/barter.html')
        
        # Check that form is in context
        self.assertIn('form', response.context_data)
        
        # Check that result is set correctly
        expected_result = ('APPLE', '1.5', 'ORANGE', '0.67', '5.50', '8.25')
        self.assertEqual(response.context_data['result'], expected_result)
        
        # Verify compare was called with uppercase crop names
        mock_compare.assert_called_once_with('APPLE - CARTON', 'ORANGE - BOX')
    
    @patch('main.views.compare')
    def test_barter_view_post_invalid(self, mock_compare):
        """Test barter view with invalid POST request"""
        # Create a POST request with invalid data (empty fields)
        request = RequestFactory().post('/barter/', {
            'crop1': '',
            'crop2': ''
        })
        
        # Call the view
        response = barter(request)
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'main/barter.html')
        
        # Check that form is in context and has errors
        self.assertIn('form', response.context_data)
        self.assertFalse(response.context_data['form'].is_valid())
        
        # Check that result is None for invalid forms
        self.assertIsNone(response.context_data['result'])
        
        # compare should not be called for invalid forms
        mock_compare.assert_not_called()


class FeedbackViewTest(TestCase):
    
    def test_feedback_view_get(self):
        """Test feedback view with GET request"""
        # Create a GET request
        request = RequestFactory().get('/feedback/')
        
        # Call the view
        response = feedback_view(request)
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'main/feedback.html')
        
        # Check that form is in context
        self.assertIn('form', response.context_data)
        self.assertIsInstance(response.context_data['form'], FeedbackForm)
    
    def test_feedback_view_post_valid(self):
        """Test feedback view with valid POST request"""
        # Create a POST request with valid data
        request = RequestFactory().post('/feedback/', {
            'name': 'John Doe',
            'message': 'Great website!'
        })
        
        # Call the view
        response = feedback_view(request)
        
        # Check that it redirects to thank you page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/feedback/thank-you/')  # Adjust based on your actual URL name
        
        # Check that feedback was saved to database
        self.assertEqual(Feedback.objects.count(), 1)
        feedback = Feedback.objects.first()
        self.assertEqual(feedback.name, 'John Doe')
        self.assertEqual(feedback.message, 'Great website!')
    
    def test_feedback_view_post_invalid(self):
        """Test feedback view with invalid POST request"""
        # Create a POST request with invalid data (missing message)
        request = RequestFactory().post('/feedback/', {
            'name': 'John Doe',
            'message': ''
        })
        
        # Call the view
        response = feedback_view(request)
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'main/feedback.html')
        
        # Check that form is in context and has errors
        self.assertIn('form', response.context_data)
        self.assertFalse(response.context_data['form'].is_valid())
        
        # Check that no feedback was saved to database
        self.assertEqual(Feedback.objects.count(), 0)


class InboxViewTest(TestCase):
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create some test feedback messages
        Feedback.objects.create(name='User1', message='Message 1')
        Feedback.objects.create(name='User2', message='Message 2')
    
    def test_inbox_view_requires_login(self):
        """Test that inbox view requires login"""
        # Create a request without authentication
        request = RequestFactory().get('/inbox/')
        
        # Call the view - should redirect to login
        response = inbox_view(request)
        
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_inbox_view_authenticated(self):
        """Test inbox view with authenticated user"""
        # Create a request with authentication
        request = RequestFactory().get('/inbox/')
        request.user = self.user
        
        # Call the view
        response = inbox_view(request)
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'main/inbox.html')
        
        # Check that messages are in context and ordered by created_at descending
        self.assertIn('messages', response.context_data)
        messages = response.context_data['messages']
        self.assertEqual(messages.count(), 2)
    
    def test_inbox_view_ordering(self):
        """Test that messages are ordered by created_at descending"""
        # Create a request with authentication
        request = RequestFactory().get('/inbox/')
        request.user = self.user
        
        # Call the view
        response = inbox_view(request)
        
        # Check that messages are ordered correctly
        messages = response.context_data['messages']
        self.assertEqual(messages[0].message, 'Message 2')  # Most recent first
        self.assertEqual(messages[1].message, 'Message 1')