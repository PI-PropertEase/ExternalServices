from fastapi import APIRouter, HTTPException
from typing import List
from base_schemas.reservation import ReservationBase, ReservationInDB, ReservationStatus, ReservationBaseUpdate
from datetime import datetime
from threading import Lock
from api_clickandgo.v1.properties import data
from pydantic import EmailStr

reservation_data = {
    1: ReservationInDB(id=1, property_id=10, client_email="smith_john@gmail.com", client_name="John Smith",
                       client_phone="+351961555555",
                       arrival=datetime(2024, 3, 14, 12, 0), departure=datetime(2024, 3, 16, 12, 0), cost=200.0,
                       reservation_status=ReservationStatus.CONFIRMED),
    2: ReservationInDB(id=2, property_id=9, client_email="doe_jane@gmail.com", client_name="Jane Doe",
                       client_phone="+351961666666",
                       arrival=datetime(2024, 4, 15, 12, 0), departure=datetime(2024, 4, 18, 12, 0), cost=220.0,
                       reservation_status=ReservationStatus.CONFIRMED),
    3: ReservationInDB(id=3, property_id=8, client_email="brown_alice@gmail.com", client_name="Alice Brown",
                       client_phone="+351961777777",
                       arrival=datetime(2024, 4, 16, 12, 0), departure=datetime(2024, 4, 19, 12, 0), cost=190.0,
                       reservation_status=ReservationStatus.CONFIRMED),
    4: ReservationInDB(id=4, property_id=8, client_email="johnson_bob@gmail.com", client_name="Bob Johnson",
                       client_phone="+351961888888",
                       arrival=datetime(2024, 5, 17, 12, 0), departure=datetime(2024, 5, 20, 12, 0), cost=230.0,
                       reservation_status=ReservationStatus.CONFIRMED),
    5: ReservationInDB(id=5, property_id=7, client_email="wilson_emily@gmail.com", client_name="Emily Wilson",
                       client_phone="+351961999999",
                       arrival=datetime(2024, 6, 8, 12, 0), departure=datetime(2024, 6, 11, 12, 0), cost=210.0,
                       reservation_status=ReservationStatus.CONFIRMED),
    6: ReservationInDB(id=6, property_id=6, client_email="martinez_michael@gmail.com", client_name="Michael Martinez",
                       client_phone="+351961111111",
                       arrival=datetime(2024, 4, 19, 12, 0), departure=datetime(2024, 4, 22, 12, 0), cost=240.0,
                       reservation_status=ReservationStatus.CONFIRMED),
    7: ReservationInDB(id=7, property_id=3, client_email="davis_olivia@gmail.com", client_name="Olivia Davis",
                       client_phone="+351961222222",
                       arrival=datetime(2024, 3, 20, 12, 0), departure=datetime(2024, 3, 23, 12, 0), cost=210.0,
                       reservation_status=ReservationStatus.CONFIRMED),
    8: ReservationInDB(id=8, property_id=2, client_email="garcia_david@gmail.com", client_name="David Garcia",
                       client_phone="+351961333333",
                       arrival=datetime(2024, 3, 21, 12, 0), departure=datetime(2024, 3, 24, 12, 0), cost=260.0,
                       reservation_status=ReservationStatus.CONFIRMED),
    9: ReservationInDB(id=9, property_id=1, client_email="rodriguez_sophia@gmail.com", client_name="Sophia Rodriguez",
                       client_phone="+351961444444",
                       arrival=datetime(2024, 3, 22, 12, 0), departure=datetime(2024, 3, 25, 12, 0), cost=220.0,
                       reservation_status=ReservationStatus.CONFIRMED),
    10: ReservationInDB(id=10, property_id=10, client_email="hernandez_james@gmail.com", client_name="James Hernandez",
                        client_phone="+351961115555",
                        arrival=datetime(2024, 3, 23, 12, 0), departure=datetime(2024, 3, 26, 12, 0), cost=280.0,
                        reservation_status=ReservationStatus.CONFIRMED),
}

lock = Lock()

sequence_id = 10

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"]
)


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
    return reservation_in_db


@router.put("/{reservation_id}", status_code=200)
def update_reservation(reservation_id: int, reservation_update_data: ReservationBaseUpdate) -> ReservationInDB:
    if not (reservation_to_update := reservation_data.get(reservation_id)):
        raise HTTPException(status_code=404, detail="Reservation doesn't exist")
    update_parameters = {field_name: field_value for field_name, field_value in reservation_update_data if
                         field_value is not None}
    updated_reservation = reservation_to_update.model_copy(update=update_parameters)
    reservation_data[reservation_id] = updated_reservation
    return updated_reservation


@router.delete("/{reservation_id}", status_code=200)
def delete_reservation(reservation_id: int) -> List[ReservationInDB]:
    del reservation_data[reservation_id]
    return reservation_data.values()
