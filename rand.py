import requests
import random
from faker import Faker

fake = Faker()

BASE_URL = "http://127.0.0.1:8000"  

def create_state():
    state_data = {
        "name": fake.country(),
        "capital": fake.city(),
        "government_type": random.choice(["Democracy", "Monarchy", "Republic", "Dictatorship"])
    }
    response = requests.post(f"{BASE_URL}/states/", json=state_data)
    if response.status_code == 200:
        print(f"Государство создано: {state_data['name']}")
        return response.json()
    else:
        print(f"Не удалось создать государство: {state_data['name']}")
        return None


