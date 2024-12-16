from datetime import datetime
from app.utils import load_category_list

def validate_transaction(transaction):
    errors = []
    
    # Validate trans_date
    try:
        datetime.strptime(transaction['trans_date'], '%Y-%m-%d')
    except ValueError:
        errors.append('Invalid trans_date format')

    # Validate trans_time
    try:
        datetime.strptime(transaction['trans_time'], '%H:%M:%S')
    except ValueError:
        errors.append('Invalid trans_time format')

    # Validate category
    categories = load_category_list()
    if transaction['category'] not in categories:
        errors.append('Invalid category')

    # Validate amount
    if not isinstance(transaction['amt'], (int, float)) or transaction['amt'] <= 0:
        errors.append('Invalid amount')

    # Validate dob
    try:
        datetime.strptime(transaction['dob'], '%Y-%m-%d')
    except ValueError:
        errors.append('Invalid dob format')

    return errors
