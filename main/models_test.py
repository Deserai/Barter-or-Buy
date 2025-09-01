from django.test import TestCase
from django.db import models
from .models import Feedback
from datetime import datetime
from unittest.mock import patch


class FeedbackModelTest(TestCase):

    def test_feedback_model_exists(self):
        """Test that the Feedback model is defined"""
        self.assertTrue(hasattr(Feedback, 'objects'))
    
    def test_model_fields(self):
        """Test that the Feedback model has the correct fields"""
        # Get all field names
        field_names = [field.name for field in Feedback._meta.get_fields()]
        
        # Check that all expected fields exist
        self.assertIn('id', field_names)
        self.assertIn('name', field_names)
        self.assertIn('message', field_names)
        self.assertIn('created_at', field_names)
    
    def test_name_field_properties(self):
        """Test the properties of the name field"""
        name_field = Feedback._meta.get_field('name')
        
        # Test field type
        self.assertIsInstance(name_field, models.CharField)
        
        # Test max_length
        self.assertEqual(name_field.max_length, 100)
        
        # Test blank property
        self.assertTrue(name_field.blank)
        
        # Test null property
        self.assertTrue(name_field.null)
    
    def test_message_field_properties(self):
        """Test the properties of the message field"""
        message_field = Feedback._meta.get_field('message')
        
        # Test field type
        self.assertIsInstance(message_field, models.TextField)
        
        # Test blank property (should be False by default)
        self.assertFalse(message_field.blank)
        
        # Test null property (should be False by default)
        self.assertFalse(message_field.null)
    
    def test_created_at_field_properties(self):
        """Test the properties of the created_at field"""
        created_at_field = Feedback._meta.get_field('created_at')
        
        # Test field type
        self.assertIsInstance(created_at_field, models.DateTimeField)
        
        # Test auto_now_add property
        self.assertTrue(created_at_field.auto_now_add)
    
    def test_create_feedback_with_name_and_message(self):
        """Test creating a Feedback instance with both name and message"""
        feedback = Feedback.objects.create(
            name="John Doe",
            message="This is a test feedback message."
        )
        
        # Check that the object was created
        self.assertIsNotNone(feedback.id)
        self.assertEqual(feedback.name, "John Doe")
        self.assertEqual(feedback.message, "This is a test feedback message.")
        self.assertIsInstance(feedback.created_at, datetime)
    
    def test_create_feedback_with_message_only(self):
        """Test creating a Feedback instance with message only (name is optional)"""
        feedback = Feedback.objects.create(
            message="This is an anonymous feedback message."
        )
        
        # Check that the object was created
        self.assertIsNotNone(feedback.id)
        self.assertIsNone(feedback.name)
        self.assertEqual(feedback.message, "This is an anonymous feedback message.")
        self.assertIsInstance(feedback.created_at, datetime)
    
    def test_create_feedback_with_empty_name(self):
        """Test creating a Feedback instance with empty string name"""
        feedback = Feedback.objects.create(
            name="",
            message="This is a test feedback message."
        )
        
        # Check that the object was created
        self.assertIsNotNone(feedback.id)
        self.assertEqual(feedback.name, "")
        self.assertEqual(feedback.message, "This is a test feedback message.")
    
    def test_str_method_with_name(self):
        """Test the __str__ method when name is provided"""
        feedback = Feedback.objects.create(
            name="Jane Smith",
            message="Great website!"
        )
        
        expected_str = "Message from Jane Smith"
        self.assertEqual(str(feedback), expected_str)
    
    def test_str_method_without_name(self):
        """Test the __str__ method when name is not provided"""
        feedback = Feedback.objects.create(
            message="Great website!"
        )
        
        expected_str = "Message from Anonymous"
        self.assertEqual(str(feedback), expected_str)
    
    def test_str_method_with_empty_name(self):
        """Test the __str__ method when name is empty string"""
        feedback = Feedback.objects.create(
            name="",
            message="Great website!"
        )
        
        expected_str = "Message from Anonymous"
        self.assertEqual(str(feedback), expected_str)
    
    def test_ordering(self):
        """Test that Feedback objects are ordered by created_at"""
        # Create feedback objects with different timestamps
        with patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = datetime(2023, 1, 1, 10, 0, 0)
            feedback1 = Feedback.objects.create(message="First message")
            
            mock_now.return_value = datetime(2023, 1, 1, 10, 30, 0)
            feedback2 = Feedback.objects.create(message="Second message")
            
            mock_now.return_value = datetime(2023, 1, 1, 11, 0, 0)
            feedback3 = Feedback.objects.create(message="Third message")
        
        # Get all feedback objects
        all_feedback = list(Feedback.objects.all())
        
        # Check that they are ordered by created_at (ascending)
        self.assertEqual(all_feedback[0], feedback1)
        self.assertEqual(all_feedback[1], feedback2)
        self.assertEqual(all_feedback[2], feedback3)
    
    def test_database_constraints(self):
        """Test that database constraints work correctly"""
        # Should not be able to create feedback without message
        with self.assertRaises(Exception):
            Feedback.objects.create(name="Test User")
    
    def test_model_verbose_names(self):
        """Test the verbose names of the model"""
        self.assertEqual(Feedback._meta.verbose_name, "feedback")
        self.assertEqual(Feedback._meta.verbose_name_plural, "feedback")
    
    def test_field_verbose_names(self):
        """Test the verbose names of the fields"""
        name_field = Feedback._meta.get_field('name')
        message_field = Feedback._meta.get_field('message')
        created_at_field = Feedback._meta.get_field('created_at')
        
        # Django automatically creates verbose names from field names
        self.assertEqual(name_field.verbose_name, "name")
        self.assertEqual(message_field.verbose_name, "message")
        self.assertEqual(created_at_field.verbose_name, "created at")