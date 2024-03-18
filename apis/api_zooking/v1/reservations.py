from fastapi import APIRouter
from typing import Dict, List
from base_schemas.reservation import ReservationBase, ReservationInDB
from datetime import datetime
from threading import Lock

reservation_data = {
    1: ReservationBase(property_id=1, status="OnGoing", client_name="John Doe", client_phone="1234567890",
                       arrival=datetime(2024, 3, 14, 12, 0), departure=datetime(2024, 3, 16, 12, 0), cost=150.0),
    2: ReservationBase(property_id=1, status="Pending", client_name="Jane Smith", client_phone="9876543210",
                       arrival=datetime(2024, 3, 16, 12, 0), departure=datetime(2024, 3, 18, 12, 0), cost=200.0),
    3: ReservationBase(property_id=1, status="OnGoing", client_name="Alice Johnson", client_phone="5551234567",
                       arrival=datetime(2024, 3, 18, 12, 0), departure=datetime(2024, 3, 19, 12, 0), cost=180.0),
    4: ReservationBase(property_id=1, status="Pending", client_name="Bob Brown", client_phone="5559876543",
                       arrival=datetime(2024, 3, 19, 12, 0), departure=datetime(2024, 3, 20, 12, 0), cost=220.0),
    5: ReservationBase(property_id=2, status="OnGoing", client_name="Emily Davis", client_phone="5552223333",
                       arrival=datetime(2024, 3, 18, 12, 0), departure=datetime(2024, 3, 21, 12, 0), cost=190.0),
    6: ReservationBase(property_id=3, status="Pending", client_name="Michael Wilson", client_phone="5554445555",
                       arrival=datetime(2024, 3, 19, 12, 0), departure=datetime(2024, 3, 22, 12, 0), cost=230.0),
    7: ReservationBase(property_id=4, status="OnGoing", client_name="Olivia Martinez", client_phone="5556667777",
                       arrival=datetime(2024, 3, 20, 12, 0), departure=datetime(2024, 3, 23, 12, 0), cost=200.0),
    8: ReservationBase(property_id=5, status="Pending", client_name="David Garcia", client_phone="5558889999",
                       arrival=datetime(2024, 3, 21, 12, 0), departure=datetime(2024, 3, 24, 12, 0), cost=250.0),
    9: ReservationBase(property_id=5, status="OnGoing", client_name="Sophia Rodriguez", client_phone="5551112222",
                       arrival=datetime(2024, 3, 22, 12, 0), departure=datetime(2024, 3, 25, 12, 0), cost=210.0),
    10: ReservationBase(property_id=6, status="Pending", client_name="James Hernandez", client_phone="5553334444",
                        arrival=datetime(2024, 3, 23, 12, 0), departure=datetime(2024, 3, 26, 12, 0), cost=270.0),
    11: ReservationBase(property_id=6, status="OnGoing", client_name="Isabella Lopez", client_phone="5555556666",
                        arrival=datetime(2024, 3, 24, 12, 0), departure=datetime(2024, 3, 27, 12, 0), cost=220.0),
    12: ReservationBase(property_id=6, status="Pending", client_name="Alexander Perez", client_phone="5557778888",
                        arrival=datetime(2024, 3, 25, 12, 0), departure=datetime(2024, 3, 28, 12, 0), cost=280.0),
    13: ReservationBase(property_id=7, status="OnGoing", client_name="Mia Gonzales", client_phone="5559990000",
                        arrival=datetime(2024, 3, 26, 12, 0), departure=datetime(2024, 3, 29, 12, 0), cost=230.0),
    14: ReservationBase(property_id=8, status="Pending", client_name="Ethan Torres", client_phone="5552221111",
                        arrival=datetime(2024, 3, 27, 12, 0), departure=datetime(2024, 3, 30, 12, 0), cost=290.0),
    15: ReservationBase(property_id=8, status="OnGoing", client_name="Charlotte Ramirez", client_phone="5558887777",
                        arrival=datetime(2024, 3, 28, 12, 0), departure=datetime(2024, 3, 31, 12, 0), cost=240.0),
    16: ReservationBase(property_id=9, status="Pending", client_name="Benjamin Flores", client_phone="5551110000",
                        arrival=datetime(2024, 3, 29, 12, 0), departure=datetime(2024, 4, 1, 12, 0), cost=300.0)
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
        id = len(reservation_data)+1
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