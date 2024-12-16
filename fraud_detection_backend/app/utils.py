import json
import pickle
from datetime import datetime
import pandas as pd

def load_category_list():
    with open('config/category_list.json', 'r') as f:
        return json.load(f)

def load_time_category_encoding():
    with open('config/time_category_encoding.json', 'r') as f:
        return json.load(f)

def load_scaler():
    with open('config/scaler.pkl', 'rb') as f:
        return pickle.load(f)

def load_model():
    with open('config/random_forest_adasyn.pkl', 'rb') as f:
        return pickle.load(f)

def categorize_time(hour):
    if 5 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 17:
        return 'afternoon'
    elif 17 <= hour < 21:
        return 'evening'
    else:
        return 'midnight'

def calculate_age(dob):
    today = datetime.now()
    born = datetime.strptime(dob, '%Y-%m-%d')
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
