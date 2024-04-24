from fastapi import APIRouter
from typing import List
from base_schemas.reservation import ReservationBase, ReservationInDB
from datetime import datetime
from threading import Lock
from api_earthstayin.v1.properties import data

reservation_data = {
    1: ReservationInDB(id=1, property_id=10, client_email="harry_larry@gmail.com", client_name="Harry Larry", client_phone="+351915555555",
                       arrival=datetime(2024, 3, 4, 12, 0), departure=datetime(2024, 3, 7, 12, 0), cost=200.0),
    2: ReservationInDB(id=2, property_id=9, client_email="janet_maven@gmail.com", client_name="Janet Maven", client_phone="+351916666666",
                       arrival=datetime(2024, 3, 3, 12, 0), departure=datetime(2024, 3, 8, 12, 0), cost=220.0),
    3: ReservationInDB(id=3, property_id=8, client_email="james_brown@gmail.com", client_name="James L. Brown", client_phone="+351917777777",
                       arrival=datetime(2024, 3, 6, 12, 0), departure=datetime(2024, 5, 9, 12, 0), cost=190.0),
    4: ReservationInDB(id=4, property_id=8, client_email="dalton_johnson@gmail.com", client_name="Dalton Johnson", client_phone="+351911888888",
                       arrival=datetime(2024, 5, 9, 12, 0), departure=datetime(2024, 5, 10, 12, 0), cost=230.0),
}

lock = Lock()


router = APIRouter(
    prefix="/reservations",
    tags=["reservations"]
)


@router.get("", status_code=200)
def get_reservations(email: str = "") -> List[ReservationInDB]:
    if(email != ""):
        properties_ids = [key for key, property in data.items() if property.user_email == email]
        return [reservation for reservation in reservation_data.values() if reservation.property_id in properties_ids]
    return reservation_data.values()


@router.get("/{property_id}", status_code=200)
def get_reservations_by_property_id(property_id: int) -> List[ReservationInDB]:
    return [reservation for reservation in reservation_data.values() if reservation.property_id == property_id]


@router.post("", status_code=201)
def create_reservation(reservation: ReservationBase) -> ReservationInDB:
    with lock:
        last_id = list(reservation_data.keys())[-1]
        id = last_id + 1
        reservation_in_db = ReservationInDB(
            property_id=reservation.property_id,
            status=reservation.status,
            client_name=reservation.client_name,
            client_phone=reservation.client_phone,
            arrival=reservation.arrival,
            departure=reservation.departure,
            cost=reservation.cost,
            id=id
        )
        reservation_data[id] = reservation_in_db
    saved_reservation = reservation_data[id]
    return saved_reservation


@router.put("/{reservation_id}", status_code=200)
def update_reservation(reservation_id: int, reservation: ReservationBase) -> ReservationInDB:
    reservation_in_db = ReservationInDB(
        property_id=reservation.property_id,
        status=reservation.status,
        client_name=reservation.client_name,
        client_phone=reservation.client_phone,
        arrival=reservation.arrival,
        departure=reservation.departure,
        cost=reservation.cost,
        id=reservation_id
    )
    reservation_data[reservation_id] = reservation_in_db
    saved_reservation = reservation_data[reservation_id]
    return saved_reservation


@router.delete("/{reservation_id}", status_code=200)
def delete_reservation(reservation_id: int) -> List[ReservationInDB]:
    del reservation_data[reservation_id]
    return reservation_data.values()