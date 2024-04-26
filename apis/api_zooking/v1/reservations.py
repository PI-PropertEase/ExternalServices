from fastapi import APIRouter, HTTPException
from typing import List
from base_schemas.reservation import ReservationBase, ReservationInDB, ReservationStatus, ReservationBaseUpdate
from datetime import datetime
from threading import Lock
from api_zooking.v1.properties import data
from pydantic import EmailStr

reservation_data = {
    1: ReservationInDB(id=1, property_id=1, client_email="john@gmail.com", client_name="John Doe",
                       client_phone="+351911234567",
                       arrival=datetime(2024, 3, 14, 12, 0), departure=datetime(2024, 3, 16, 12, 0), cost=150.0,
                       reservation_status=ReservationStatus.CONFIRMED),
    2: ReservationInDB(id=2, property_id=1, client_email="jane@gmail.com", client_name="Jane Smith",
                       client_phone="+351916543210",
                       arrival=datetime(2024, 3, 16, 12, 0), departure=datetime(2024, 3, 18, 12, 0), cost=200.0,
                       reservation_status=ReservationStatus.CONFIRMED),
    3: ReservationInDB(id=3, property_id=1, client_email="alice@gmail.com", client_name="Alice Johnson",
                       client_phone="+351961234567",
                       arrival=datetime(2024, 3, 18, 12, 0), departure=datetime(2024, 3, 19, 12, 0), cost=180.0,
                       reservation_status=ReservationStatus.CONFIRMED),
    4: ReservationInDB(id=4, property_id=1, client_email="bob@gmail.com", client_name="Bob Brown",
                       client_phone="+351929876543",
                       arrival=datetime(2024, 3, 19, 12, 0), departure=datetime(2024, 3, 20, 12, 0), cost=220.0,
                       reservation_status=ReservationStatus.CONFIRMED),
    5: ReservationInDB(id=5, property_id=2, client_email="emily@gmail.com", client_name="Emily Davis",
                       client_phone="+351235222333",
                       arrival=datetime(2024, 3, 18, 12, 0), departure=datetime(2024, 3, 21, 12, 0), cost=190.0,
                       reservation_status=ReservationStatus.CONFIRMED),
    6: ReservationInDB(id=6, property_id=3, client_email="michael@gmail.com", client_name="Michael Wilson",
                       client_phone="+351915444555",
                       arrival=datetime(2024, 3, 19, 12, 0), departure=datetime(2024, 3, 22, 12, 0), cost=230.0,
                       reservation_status=ReservationStatus.CONFIRMED),
    7: ReservationInDB(id=7, property_id=4, client_email="olivia@gmail.com", client_name="Olivia Martinez",
                       client_phone="+351925666777",
                       arrival=datetime(2024, 3, 20, 12, 0), departure=datetime(2024, 3, 23, 12, 0), cost=200.0,
                       reservation_status=ReservationStatus.CONFIRMED),
    8: ReservationInDB(id=8, property_id=5, client_email="david@gmail.com", client_name="David Garcia",
                       client_phone="+351915888999",
                       arrival=datetime(2024, 3, 21, 12, 0), departure=datetime(2024, 3, 24, 12, 0), cost=250.0,
                       reservation_status=ReservationStatus.CONFIRMED),
    9: ReservationInDB(id=9, property_id=5, client_email="sophia@gmail.com", client_name="Sophia Rodriguez",
                       client_phone="+351965111222",
                       arrival=datetime(2024, 3, 24, 12, 0), departure=datetime(2024, 3, 25, 12, 0), cost=210.0,
                       reservation_status=ReservationStatus.CONFIRMED),
    10: ReservationInDB(id=10, property_id=6, client_email="james@gmail.com", client_name="James Hernandez",
                        client_phone="+351235333444",
                        arrival=datetime(2024, 3, 23, 12, 0), departure=datetime(2024, 3, 26, 12, 0), cost=270.0,
                        reservation_status=ReservationStatus.CONFIRMED),
    11: ReservationInDB(id=11, property_id=6, client_email="isabella@gmail.com", client_name="Isabella Lopez",
                        client_phone="+351915555666",
                        arrival=datetime(2024, 3, 26, 12, 0), departure=datetime(2024, 3, 27, 12, 0), cost=220.0,
                        reservation_status=ReservationStatus.CONFIRMED),
    12: ReservationInDB(id=12, property_id=6, client_email="alexander@gmail.com", client_name="Alexander Perez",
                        client_phone="+351965777888",
                        arrival=datetime(2024, 3, 27, 12, 0), departure=datetime(2024, 3, 28, 12, 0), cost=280.0,
                        reservation_status=ReservationStatus.CONFIRMED),
    13: ReservationInDB(id=13, property_id=7, client_email="mia@gmail.com", client_name="Mia Gonzales",
                        client_phone="+351965999000",
                        arrival=datetime(2024, 3, 26, 12, 0), departure=datetime(2024, 3, 29, 12, 0), cost=230.0,
                        reservation_status=ReservationStatus.CONFIRMED),
    14: ReservationInDB(id=14, property_id=8, client_email="ethan@gmail.com", client_name="Ethan Torres",
                        client_phone="+351915222111",
                        arrival=datetime(2024, 3, 27, 12, 0), departure=datetime(2024, 3, 30, 12, 0), cost=290.0,
                        reservation_status=ReservationStatus.CONFIRMED),
    15: ReservationInDB(id=15, property_id=8, client_email="charlotte@gmail.com", client_name="Charlotte Ramirez",
                        client_phone="+351965888777",
                        arrival=datetime(2024, 3, 30, 12, 0), departure=datetime(2024, 3, 31, 12, 0), cost=240.0,
                        reservation_status=ReservationStatus.CONFIRMED),
    16: ReservationInDB(id=16, property_id=9, client_email="benjamin@gmail.com", client_name="Benjamin Flores",
                        client_phone="+352455111000",
                        arrival=datetime(2024, 3, 29, 12, 0), departure=datetime(2024, 4, 1, 12, 0), cost=300.0,
                        reservation_status=ReservationStatus.CONFIRMED)
}

lock = Lock()

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"]
)

sequence_id = 17


@router.get("", status_code=200)
def get_reservations(email: str = "") -> List[ReservationInDB]:
    if (email != ""):
        properties_ids = [key for key, property in data.items() if property.user_email == email]
        return [reservation for reservation in reservation_data.values() if reservation.property_id in properties_ids]
    return reservation_data.values()


@router.get("/upcoming", status_code=200)
def get_upcoming_reservations(email: EmailStr):
    properties_ids = [key for key, property in data.items() if property.user_email == email]
    if email == "miguel9bf@gmail.com":
        properties_ids = [1]
    return [reservation for reservation in reservation_data.values() if reservation.property_id in properties_ids
            and reservation.arrival > datetime.now()]


@router.get("/{property_id}", status_code=200)
def get_reservations_by_property_id(property_id: int) -> List[ReservationInDB]:
    return [reservation for reservation in reservation_data.values() if reservation.property_id == property_id]


@router.post("", status_code=201)
def create_reservation(reservation: ReservationBase) -> ReservationInDB:
    global sequence_id
    with lock:
        sequence_id += 1
        reservation_in_db = ReservationInDB(
            property_id=reservation.property_id,
            client_email=reservation.client_email,
            client_name=reservation.client_name,
            client_phone=reservation.client_phone,
            arrival=reservation.arrival,
            departure=reservation.departure,
            cost=reservation.cost,
            reservation_status=reservation.reservation_status,
            id=sequence_id
        )
        reservation_data[sequence_id] = reservation_in_db
        sequence_id += 1
    return reservation_in_db


@router.put("/{reservation_id}", status_code=200)
def update_reservation(reservation_id: int, reservation_update_data: ReservationBaseUpdate) -> ReservationInDB:
    if not (reservation_to_update := reservation_data.get(reservation_id)):
        raise HTTPException(status_code=404, detail="Reservation doesn't exist")
    update_parameters = {field_name: field_value for field_name, field_value in reservation_update_data if field_value is not None}
    updated_reservation = reservation_to_update.model_copy(update=update_parameters)
    reservation_data[reservation_id] = updated_reservation
    return updated_reservation


@router.delete("/{reservation_id}", status_code=200)
def delete_reservation(reservation_id: int) -> List[ReservationInDB]:
    del reservation_data[reservation_id]
    return reservation_data.values()
