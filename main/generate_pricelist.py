import os
import re
import pandas as pd
from django.conf import settings


CSV_PATH = os.path.join(settings.BASE_DIR, 'main/data', '01_09_2025.csv')


def load_dataframe():
    """
        Reads the csv pricelist.
        Returns an edited dataframe of the pricelist.
    """
    try:
        df=pd.read_csv(CSV_PATH, encoding='utf-8')
        df['DESC'] = df['DESC'].apply(lambda x: re.sub(r'["]', '', x.upper()))
        df['CONTAINER'] = df['CONTAINER'].apply(lambda x: re.sub(r'["]', '', x.upper()))
        return df
    
    except Exception as e:
        print("Error loading CSV", e)
        return pd.DataFrame()


df = load_dataframe()

    
def get_matching_crops(crop):
    """ 
        Takes in a crop name as an argument.
        Returns a list of crops that matches the argument from the crop pricelist.
    """
    if df.empty or 'DESC' not in df.columns:
        return []

    try:
        display_matches = df['DESC'] + " - " + df['CONTAINER']
        matches = display_matches[display_matches.str.contains(crop, case=False, na=False)]
        unqiue_value = set(matches)
        return list(unqiue_value)
    except (ValueError, IndexError):
        return "Please enter a longer word"


def priceOf(crop):
    """ 
        Takes in a crop name as an argument.
        Returns the price crop that matches the argument from the crop pricelist.
    """
    display_matches = df['DESC'] + " - " + df['CONTAINER']
    crop_list = list(display_matches)
    if crop in crop_list:
        crop_index = display_matches[display_matches == crop].index[0]
        crop_mass = float(df.iloc[crop_index]['MASS'])
        crop_price = float(df.iloc[crop_index]['AVERAGE PRICE'])
        try:
            price_per_kg = crop_price / crop_mass
            return f'{price_per_kg:.2f}'
        except (ValueError, IndexError):
            return "error"
    else: 
        return None


def compare(crop1, crop2):
    """ 
        Takes in two crop names as arguments.
        Returns the price of crops and 
        the comparsion between the two crops in weight and price.
    """
    display_matches = df['DESC'] + " - " + df['CONTAINER']
    crop_list = list(display_matches)
    if crop1 in crop_list and crop2 in crop_list:
        price1 = priceOf(crop1)  
        price2 = priceOf(crop2)
        x = float(price1)
        y = float(price2)
        try:
            first_comparsion = x / y
            second_comparsion =  y / x
            result = (crop1.title(), f'{first_comparsion:.2f}', 
                    crop2.title(), f'{second_comparsion:.2f}',
                    f'{x:.2f}',f'{y:.2f}')
            return result
        except (ValueError, IndexError):
            return "Error comparing prices."
    else: 
        return None
    