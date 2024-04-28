from fastapi import APIRouter, HTTPException
from typing import List
from base_schemas.reservation import ReservationBase, ReservationInDB, ReservationStatus, ReservationBaseUpdate
from datetime import datetime
from threading import Lock
from api_earthstayin.v1.properties import data
from pydantic import EmailStr

reservation_data = {
    1: ReservationInDB(id=1, property_id=10, client_email="harry_larry@gmail.com", client_name="Harry Larry",
                       client_phone="+351915555555",
                       arrival=datetime(2024, 3, 4, 12, 0), departure=datetime(2024, 3, 7, 12, 0), cost=200.0,
                       reservation_status=ReservationStatus.CONFIRMED),
    2: ReservationInDB(id=2, property_id=9, client_email="janet_maven@gmail.com", client_name="Janet Maven",
                       client_phone="+351916666666",
                       arrival=datetime(2024, 3, 3, 12, 0), departure=datetime(2024, 3, 8, 12, 0), cost=220.0,
                       reservation_status=ReservationStatus.CONFIRMED),
    3: ReservationInDB(id=3, property_id=8, client_email="james_brown@gmail.com", client_name="James L. Brown",
                       client_phone="+351917777777",
                       arrival=datetime(2024, 3, 6, 12, 0), departure=datetime(2024, 5, 9, 12, 0), cost=190.0,
                       reservation_status=ReservationStatus.CONFIRMED),
    4: ReservationInDB(id=4, property_id=8, client_email="dalton_johnson@gmail.com", client_name="Dalton Johnson",
                       client_phone="+351911888888",
                       arrival=datetime(2024, 5, 9, 12, 0), departure=datetime(2024, 5, 10, 12, 0), cost=230.0,
                       reservation_status=ReservationStatus.CONFIRMED),
}

lock = Lock()

sequence_id = 4

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
