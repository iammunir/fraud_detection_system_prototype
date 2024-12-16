from app.celery_app import celery_app
from app.utils import (
    categorize_time, calculate_age, load_category_list,
    load_time_category_encoding, load_scaler, load_model
)
from app.models import Transaction, engine
from app.rethink import r, connect_rethink
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

@celery_app.task(name='preprocessing')
def preprocess_transaction(transactions):
    for transaction in transactions:
        # Create new fields
        trans_datetime = datetime.strptime(
            f"{transaction['trans_date']} {transaction['trans_time']}", 
            '%Y-%m-%d %H:%M:%S'
        )

        time_category = categorize_time(trans_datetime.hour)
        
        processed_transaction = {
            'amt': transaction['amt'],
            'transaction_month': trans_datetime.month,
            'transaction_day': trans_datetime.day,
            'transaction_hour': trans_datetime.hour,
            'transaction_day_of_week': trans_datetime.weekday(),
            'transaction_is_weekend': trans_datetime.weekday() >= 5,
            'age': calculate_age(transaction['dob']),
        }

        # One-hot encoding for category
        categories = load_category_list()
        for cat in categories:
            processed_transaction[f'cat_{cat}'] = transaction['category'] == cat

        # Encode time category
        time_category_encoding = load_time_category_encoding()
        processed_transaction['time_category_encoded'] = time_category_encoding[time_category]

        # Scale numerical fields
        scaler = load_scaler()
        numerical_features = ['amt', 'age']
        scaled_values = scaler.transform([[processed_transaction[f] for f in numerical_features]])
        for i, f in enumerate(numerical_features):
            processed_transaction[f] = scaled_values[0][i]

        predict_transaction.delay(transaction, processed_transaction)

@celery_app.task(name='prediction')
def predict_transaction(original_transaction, transaction):
    model = load_model()

    feature_names = model.feature_names_in_ 
    
    # Prepare features for prediction
    features = pd.DataFrame([transaction])

    # reorder features
    reordered_data = features[feature_names]

    # predict
    prediction = model.predict(reordered_data)[0]
    
    original_transaction['is_fraud'] = bool(prediction)

    # at predicted_at and lag in seconds
    trans_datetime = datetime.strptime(
            f"{original_transaction['trans_date']} {original_transaction['trans_time']}", 
            '%Y-%m-%d %H:%M:%S'
        )
    current_datetime = datetime.now()
    original_transaction['predicted_at'] = current_datetime
    original_transaction['lag_in_seconds'] = (current_datetime - trans_datetime).total_seconds()

    store_transaction.delay(original_transaction)
    monitor_transaction.delay(original_transaction)

@celery_app.task(name='storage')
def store_transaction(transaction):
    session = Session()
    try:
        db_transaction = Transaction(**transaction)
        session.add(db_transaction)
        session.commit()
    finally:
        session.close()

@celery_app.task(name='monitor')
def monitor_transaction(transaction):
    transaction['predicted_at'] = transaction['predicted_at'].strftime("%Y-%m-%d %H:%M:%S")
    try:
        rethink_conn = connect_rethink()
        r.table('transactions').insert([transaction]).run(rethink_conn)
    finally:
        rethink_conn.close()
