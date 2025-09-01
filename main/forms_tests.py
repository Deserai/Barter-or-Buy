from django.test import TestCase
from django import forms
from .forms import CropSearchForm, Compare, FeedbackForm
from .models import Feedback


class CropSearchFormTest(TestCase):
    
    def test_form_has_correct_fields(self):
        """Test that the form has the correct field"""
        form = CropSearchForm()
        self.assertIn('crop', form.fields)
    
    def test_form_field_properties(self):
        """Test the properties of the crop field"""
        form = CropSearchForm()
        crop_field = form.fields['crop']
        
        # Test field type
        self.assertIsInstance(crop_field, forms.CharField)
        
        # Test label
        self.assertEqual(crop_field.label, "Price of ")
        
        # Test max_length
        self.assertEqual(crop_field.max_length, 100)
    
    def test_form_widget_attributes(self):
        """Test the widget attributes of the crop field"""
        form = CropSearchForm()
        widget = form.fields['crop'].widget
        
        # Test widget type
        self.assertIsInstance(widget, forms.TextInput)
        
        # Test widget attributes
        self.assertEqual(widget.attrs.get('id'), 'crop')
        self.assertEqual(widget.attrs.get('class'), 'autocomplete-input')
        self.assertEqual(widget.attrs.get('autocomplete'), 'off')
        self.assertEqual(widget.attrs.get('placeholder'), 'e.g. Carrots')
    
    def test_form_validation(self):
        """Test form validation with valid and invalid data"""
        # Test valid data
        form = CropSearchForm(data={'crop': 'Carrots'})
        self.assertTrue(form.is_valid())
        
        # Test empty data
        form = CropSearchForm(data={'crop': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('crop', form.errors)
        
        # Test data that's too long
        long_string = 'a' * 101
        form = CropSearchForm(data={'crop': long_string})
        self.assertFalse(form.is_valid())
        self.assertIn('crop', form.errors)


class CompareFormTest(TestCase):
    
    def test_form_has_correct_fields(self):
        """Test that the form has the correct fields"""
        form = Compare()
        self.assertIn('crop1', form.fields)
        self.assertIn('crop2', form.fields)
    
    def test_form_field_properties(self):
        """Test the properties of the form fields"""
        form = Compare()
        
        # Test crop1 field
        crop1_field = form.fields['crop1']
        self.assertIsInstance(crop1_field, forms.CharField)
        self.assertEqual(crop1_field.label, "Compare")
        self.assertEqual(crop1_field.max_length, 100)
        
        # Test crop2 field
        crop2_field = form.fields['crop2']
        self.assertIsInstance(crop2_field, forms.CharField)
        self.assertEqual(crop2_field.label, "to")
        self.assertEqual(crop2_field.max_length, 100)
    
    def test_form_widget_attributes(self):
        """Test the widget attributes of the form fields"""
        form = Compare()
        
        # Test crop1 widget attributes
        crop1_widget = form.fields['crop1'].widget
        self.assertEqual(crop1_widget.attrs.get('id'), 'crop')
        self.assertEqual(crop1_widget.attrs.get('class'), 'autocomplete-input')
        self.assertEqual(crop1_widget.attrs.get('autocomplete'), 'off')
        self.assertEqual(crop1_widget.attrs.get('placeholder'), 'e.g. Carrot')
        
        # Test crop2 widget attributes
        crop2_widget = form.fields['crop2'].widget
        self.assertEqual(crop2_widget.attrs.get('id'), 'crop2')
        self.assertEqual(crop2_widget.attrs.get('class'), 'autocomplete-input')
        self.assertEqual(crop2_widget.attrs.get('autocomplete'), 'off')
        self.assertEqual(crop2_widget.attrs.get('placeholder'), 'e.g. Tomato')
    
    def test_form_validation(self):
        """Test form validation with valid and invalid data"""
        # Test valid data
        form = Compare(data={'crop1': 'Carrots', 'crop2': 'Tomatoes'})
        self.assertTrue(form.is_valid())
        
        # Test empty data
        form = Compare(data={'crop1': '', 'crop2': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('crop1', form.errors)
        self.assertIn('crop2', form.errors)
        
        # Test only one field empty
        form = Compare(data={'crop1': 'Carrots', 'crop2': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('crop2', form.errors)
        
        # Test data that's too long
        long_string = 'a' * 101
        form = Compare(data={'crop1': long_string, 'crop2': 'Tomatoes'})
        self.assertFalse(form.is_valid())
        self.assertIn('crop1', form.errors)


class FeedbackFormTest(TestCase):
    
    def test_form_meta_class(self):
        """Test the Meta class configuration"""
        form = FeedbackForm()
        
        # Test model
        self.assertEqual(form.Meta.model, Feedback)
        
        # Test fields
        self.assertEqual(form.Meta.fields, ['name', 'message'])
    
    def test_form_has_correct_fields(self):
        """Test that the form has the correct fields"""
        form = FeedbackForm()
        self.assertIn('name', form.fields)
        self.assertIn('message', form.fields)
    
    def test_form_field_types(self):
        """Test the field types"""
        form = FeedbackForm()
        
        # Both fields should be CharField
        self.assertIsInstance(form.fields['name'], forms.CharField)
        self.assertIsInstance(form.fields['message'], forms.CharField)
    
    def test_form_validation(self):
        """Test form validation with valid and invalid data"""
        # Test valid data
        form = FeedbackForm(data={
            'name': 'John Doe',
            'message': 'This is a test feedback message.'
        })
        self.assertTrue(form.is_valid())
        
        # Test empty data
        form = FeedbackForm(data={'name': '', 'message': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('message', form.errors)
        
        # Test only name empty
        form = FeedbackForm(data={
            'name': '',
            'message': 'This is a test feedback message.'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        
        # Test only message empty
        form = FeedbackForm(data={
            'name': 'John Doe',
            'message': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)
    
    def test_form_save(self):
        """Test that the form can save data correctly"""
        form = FeedbackForm(data={
            'name': 'Jane Smith',
            'message': 'Great website! Very useful.'
        })
        
        self.assertTrue(form.is_valid())
        
        # Save the form
        feedback = form.save()
        
        # Check that the object was created with correct data
        self.assertEqual(feedback.name, 'Jane Smith')
        self.assertEqual(feedback.message, 'Great website! Very useful.')
        
        # Check that the object was saved to the database
        self.assertIsNotNone(feedback.id)
        self.assertEqual(Feedback.objects.count(), 1)
        
        # Verify the saved object
        saved_feedback = Feedback.objects.first()
        self.assertEqual(saved_feedback.name, 'Jane Smith')
        self.assertEqual(saved_feedback.message, 'Great website! Very useful.')