from fastapi import APIRouter
from typing import Dict, List
from base_schemas.reservation import ReservationBase, ReservationInDB
from datetime import datetime
from threading import Lock

reservation_data = {
    1: ReservationBase(property_id=10, status="OnGoing", client_name="Harry Larry", client_phone="5555555555",
                       arrival=datetime(2024, 3, 4, 12, 0), departure=datetime(2024, 3, 7, 12, 0), cost=200.0),
    2: ReservationBase(property_id=9, status="Pending", client_name="Janet Maven", client_phone="6666666666",
                       arrival=datetime(2024, 3, 3, 12, 0), departure=datetime(2024, 3, 8, 12, 0), cost=220.0),
    3: ReservationBase(property_id=8, status="OnGoing", client_name="James L. Brown", client_phone="7777777777",
                       arrival=datetime(2024, 3, 6, 12, 0), departure=datetime(2024, 5, 9, 12, 0), cost=190.0),
    4: ReservationBase(property_id=8, status="Pending", client_name="Dalton Johnson", client_phone="8888888888",
                       arrival=datetime(2024, 3, 5, 12, 0), departure=datetime(2024, 3, 10, 12, 0), cost=230.0),
}

lock = Lock()


router = APIRouter(
    prefix="/reservations",
    tags=["reservations"]
)


@router.get("/", status_code=200)
def get_reservation_list() -> Dict[int, ReservationBase]:
    return reservation_data


@router.get("/{property_id}", status_code=200)
def get_reservations_by_property_id(property_id: int) -> List[ReservationBase]:
    reservations = []
    for reservation in reservation_data.values():
        if reservation.property_id == property_id:
            reservations.append(reservation)
    return reservations


@router.post("/", status_code=201)
def create_reservation(reservation: ReservationBase) -> ReservationInDB:
    with lock:
        last_id = list(reservation_data.keys())[-1]
        id = last_id + 1
        reservation_data[id] = reservation
    saved_reservation = reservation_data[id]
    reservation_in_db = ReservationInDB(
        property_id=saved_reservation.property_id,
        status=saved_reservation.status,
        client_name=saved_reservation.client_name,
        client_phone=saved_reservation.client_phone,
        arrival=saved_reservation.arrival,
        departure=saved_reservation.departure,
        cost=saved_reservation.cost,
        id=id
    )
    return reservation_in_db


@router.put("/{reservation_id}", status_code=200)
def update_reservation(reservation_id: int, reservation: ReservationBase) -> ReservationInDB:
    reservation_data[reservation_id] = reservation
    saved_reservation = reservation_data[reservation_id]
    reservation_in_db = ReservationInDB(
        property_id=saved_reservation.property_id,
        status=saved_reservation.status,
        client_name=saved_reservation.client_name,
        client_phone=saved_reservation.client_phone,
        arrival=saved_reservation.arrival,
        departure=saved_reservation.departure,
        cost=saved_reservation.cost,
        id=reservation_id
    )
    return reservation_in_db


@router.delete("/{reservation_id}", status_code=200)
def delete_reservation(reservation_id: int) -> Dict[int, ReservationBase]:
    del reservation_data[reservation_id]
    return reservation_data