import unittest
from unittest.mock import patch, mock_open
import pandas as pd
import sys
import os

# Add the path to import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the functions to test
from generate_pricelist import load_dataframe, get_matching_crops, priceOf, compare


class TestPriceListFunctions(unittest.TestCase):
    
    def setUp(self):
        """Set up test data before each test method"""
        # Sample test data that mimics the CSV structure
        self.test_data = [
            ['"Apple","RED DELICIOUS","CARTON","18.0","EXTRA FANCY","88","80.0","100.0","90.0"'],
            ['"Banana","CAVENDISH","BOX","20.0","FIRST CLASS","100","50.0","70.0","60.0"'],
            ['"Orange","NAVEL","BAG","10.0","STANDARD","40","30.0","40.0","35.0"'],
            ['"Apple","GRANNY SMITH","CARTON","15.0","EXTRA FANCY","72","70.0","90.0","80.0"']
        ]
        
        # Create a mock dataframe
        self.mock_df = pd.DataFrame({
            'ITEM': [
                ['Apple', 'RED DELICIOUS', 'CARTON', '18.0', 'EXTRA FANCY', '88', '80.0', '100.0', '90.0'],
                ['Banana', 'CAVENDISH', 'BOX', '20.0', 'FIRST CLASS', '100', '50.0', '70.0', '60.0'],
                ['Orange', 'NAVEL', 'BAG', '10.0', 'STANDARD', '40', '30.0', '40.0', '35.0'],
                ['Apple', 'GRANNY SMITH', 'CARTON', '15.0', 'EXTRA FANCY', '72', '70.0', '90.0', '80.0']
            ],
            'DESC': ['RED DELICIOUS', 'CAVENDISH', 'NAVEL', 'GRANNY SMITH'],
            'CONTAINER': ['CARTON', 'BOX', 'BAG', 'CARTON'],
            'MASS': [18.0, 20.0, 10.0, 15.0],
            'AVERAGE PRICE': [90.0, 60.0, 35.0, 80.0]
        })
    
    @patch('pandas.read_csv')
    def test_load_dataframe_success(self, mock_read_csv):
        """Test loading dataframe successfully"""
        # Mock the read_csv function to return our test data
        mock_read_csv.return_value = pd.DataFrame([x[0].split(',') for x in self.test_data])
        
        # Call the function
        result = load_dataframe()
        
        # Verify the function processed the data correctly
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)
        self.assertIn('DESC', result.columns)
        self.assertIn('CONTAINER', result.columns)
        self.assertIn('MASS', result.columns)
        self.assertIn('AVERAGE PRICE', result.columns)
    
    @patch('pandas.read_csv')
    def test_load_dataframe_file_not_found(self, mock_read_csv):
        """Test loading dataframe when file is not found"""
        # Mock the read_csv function to raise an exception
        mock_read_csv.side_effect = Exception("File not found")
        
        # Call the function
        result = load_dataframe()
        
        # Verify the function returns an empty DataFrame
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(result.empty)
    
    def test_get_matching_crops_empty_dataframe(self):
        """Test get_matching_crops with empty dataframe"""
        # Create an empty dataframe
        empty_df = pd.DataFrame()
        
        # Patch the global df variable
        with patch('generate_pricelist.df', empty_df):
            result = get_matching_crops("apple")
            
            # Should return empty list
            self.assertEqual(result, [])
    
    def test_get_matching_crops_no_desc_column(self):
        """Test get_matching_crops when DESC column doesn't exist"""
        # Create a dataframe without DESC column
        invalid_df = pd.DataFrame({'OTHER_COL': [1, 2, 3]})
        
        # Patch the global df variable
        with patch('generate_pricelist.df', invalid_df):
            result = get_matching_crops("apple")
            
            # Should return empty list
            self.assertEqual(result, [])
    
    def test_get_matching_crops_found(self):
        """Test get_matching_crops when matches are found"""
        # Patch the global df variable
        with patch('generate_pricelist.df', self.mock_df):
            result = get_matching_crops("apple")
            
            # Should return matching crops
            self.assertEqual(len(result), 2)
            self.assertIn("RED DELICIOUS - CARTON", result)
            self.assertIn("GRANNY SMITH - CARTON", result)
    
    def test_get_matching_crops_not_found(self):
        """Test get_matching_crops when no matches are found"""
        # Patch the global df variable
        with patch('generate_pricelist.df', self.mock_df):
            result = get_matching_crops("mango")
            
            # Should return empty list
            self.assertEqual(result, [])
    
    def test_priceOf_found(self):
        """Test priceOf when crop is found"""
        # Patch the global df variable
        with patch('generate_pricelist.df', self.mock_df):
            result = priceOf("RED DELICIOUS - CARTON")
            
            # Should return the correct price per kg
            expected_price = 90.0 / 18.0  # AVERAGE PRICE / MASS
            self.assertEqual(result, f"{expected_price:.2f}")
    
    def test_priceOf_not_found(self):
        """Test priceOf when crop is not found"""
        # Patch the global df variable
        with patch('generate_pricelist.df', self.mock_df):
            result = priceOf("MANGO - BOX")
            
            # Should return error message
            self.assertEqual(result, "Crop not found on list.")
    
    def test_compare_success(self):
        """Test compare with valid crops"""
        # Patch the global df variable
        with patch('generate_pricelist.df', self.mock_df):
            crop1 = "RED DELICIOUS - CARTON"
            crop2 = "CAVENDISH - BOX"
            
            result = compare(crop1, crop2)
            
            # Should return a tuple with comparison results
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 6)
            
            # Verify the prices are calculated correctly
            price1 = 90.0 / 18.0  # Apple price per kg
            price2 = 60.0 / 20.0  # Banana price per kg
            
            self.assertEqual(result[4], f"{price1:.2f}")
            self.assertEqual(result[5], f"{price2:.2f}")
    
    def test_compare_invalid_crop(self):
        """Test compare with invalid crops"""
        # Patch the global df variable
        with patch('generate_pricelist.df', self.mock_df):
            crop1 = "RED DELICIOUS - CARTON"
            crop2 = "MANGO - BOX"  # Invalid crop
            
            result = compare(crop1, crop2)
            
            # Should return error message
            self.assertEqual(result, "Error comparing prices.")


if __name__ == '__main__':
    unittest.main()