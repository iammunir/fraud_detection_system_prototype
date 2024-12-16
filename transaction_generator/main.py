import requests
import random
import time
from time import sleep
from faker import Faker
from datetime import datetime, time
import os

fake = Faker()

categories = [
    "misc_net", "grocery_pos", "entertainment", "gas_transport", "misc_pos",
    "grocery_net", "shopping_net", "shopping_pos", "food_dining", 
    "personal_care", "health_fitness", "travel", "kids_pets", "home"
]

def generate_transaction(is_fraud=False):
    trans_time = fake.time_object()
    amt = fake.pyfloat(left_digits=3, right_digits=2, positive=True)
    dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
    age = (datetime.now().date() - dob).days / 365
    category = random.choice(categories)

    if is_fraud:
        # Generate a time between midnight and 3 AM
        start_time = datetime.combine(datetime.today(), time(0, 0))
        end_time = datetime.combine(datetime.today(), time(3, 0))
        trans_time = fake.time_object(end_datetime=end_time)
        amt = random.uniform(1000, 5000)  # Larger amounts
        if age > 60 or age < 25:
            category = random.choice(["misc_net", "shopping_net", "travel"])


    gender = random.choice(["M", "F"])

    transaction = {
        "trans_num": fake.uuid4(),
        "trans_date": fake.date_this_year().strftime("%Y-%m-%d"),
        "trans_time": trans_time.strftime("%H:%M:%S"),
        "cc_num": fake.credit_card_number(),
        "merchant": fake.company(),
        "first": fake.first_name_female() if gender == "F" else fake.first_name_male(),
        "last": fake.last_name(),
        "gender": gender,
        "category": category,
        "amt": amt,
        "dob": dob.strftime("%Y-%m-%d")
    }
    return transaction

def send_transactions():
    url = os.getenv("API_URL")
    while True:
        batch_size = random.randint(1, 5)
        transactions = []
        for _ in range(batch_size):
            is_fraud = random.random() < 0.2  # 20% chance of being a fraud
            transaction = generate_transaction(is_fraud=is_fraud)
            transactions.append(transaction)
        
        response = requests.post(url, json=transactions)
        print(f"Sent {len(transactions)} transactions, Response: {response.status_code}")
        
        sleep(3)

if __name__ == "__main__":
    send_transactions()
