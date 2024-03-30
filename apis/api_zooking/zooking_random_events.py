# This script randomly calls the zooking API, creating/deleting/updating properties and reservations
import requests
from base_schemas.property import PropertyBase, PropertyInDB
from base_schemas.reservation import ReservationBase, ReservationInDB
import string
import random
from datetime import datetime
from time import sleep

PROPERTY_IDS = [i for i in range(11)]  # there are 10 properties when the server opens

ZOOKING_URL = "http://localhost:8000"  # doesn't end in /


def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits
    result = "".join(random.choice(characters) for _ in range(length))
    return result


def create_property():
    property_data = PropertyBase(
        name=generate_random_string(),
        address=generate_random_string(),
        status="Free",
        curr_price=1.0,
    )
    call_url = f"{ZOOKING_URL}/properties"
    res = requests.post(url=call_url, json=property_data.model_dump())
    print(f"POST /properties - STATUS: {res.status_code}")
    if res.status_code == 201:
        PROPERTY_IDS.append(res.json().get("id"))
    else:
        print(f"ERROR: {res.json()}")


def update_property():
    property_id = random.choice(PROPERTY_IDS)
    property_data = PropertyBase(
        name=generate_random_string(),
        address=generate_random_string(),
        status="Free",
        curr_price=1.0,
    )
    call_url = f"{ZOOKING_URL}/properties/{property_id}"
    res = requests.put(url=call_url, json=property_data.model_dump())
    print(f"PUT /properties/{property_id} - STATUS: {res.status_code}")
    if res.status_code != 200:
        print(f"ERROR: {res.json()}")


def delete_property():
    property_id = random.choice(PROPERTY_IDS)
    call_url = f"{ZOOKING_URL}/properties/{property_id}"
    res = requests.delete(url=call_url)
    print(f"DELETE /properties/{property_id} - STATUS: {res.status_code}")
    if res.status_code == 200:
        PROPERTY_IDS.remove(property_id)
    else:
        print(f"ERROR: {res.json()}")


def create_reservation():
    reservation = ReservationBase(
        property_id=random.choice(PROPERTY_IDS),
        status="Pending",
        client_name=generate_random_string(),
        client_phone=generate_random_string(9),
        arrival=datetime(2024, 4 + random.randint(1, 8), 20, 1, 1),
        departure=datetime(2024, 12, 31, 23, 59),
        cost=20.0,
    )
    call_url = f"{ZOOKING_URL}/reservations"
    res = requests.post(url=call_url, data=reservation.model_dump_json())
    print(f"POST /reservations - STATUS: {res.status_code}")
    if res.status_code != 201:
        print(f"ERROR: {res.json()}")


if __name__ == "__main__":
    while True:
        method_to_call = random.choice(
            [create_property, update_property, delete_property, create_reservation]
        )
        method_to_call()
        sleep(1)
