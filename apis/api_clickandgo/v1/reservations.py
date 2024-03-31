from fastapi import APIRouter
from typing import Dict, List
from api_clickandgo.schemas.reservation import Reservation, ReservationInDB
from datetime import datetime
from threading import Lock

reservation_data = {
    1: Reservation(property_id=10, status="OnGoing", client_name="John Smith", client_phone="5555555555",
                       arrival=datetime(2024, 3, 14, 12, 0), departure=datetime(2024, 3, 16, 12, 0), cost=200.0, amenities=["crib", "extra bed"]),
    2: Reservation(property_id=9, status="Pending", client_name="Jane Doe", client_phone="6666666666",
                       arrival=datetime(2024, 4, 15, 12, 0), departure=datetime(2024, 4, 18, 12, 0), cost=220.0, amenities=[]),
    3: Reservation(property_id=8, status="OnGoing", client_name="Alice Brown", client_phone="7777777777",
                       arrival=datetime(2024, 4, 16, 12, 0), departure=datetime(2024, 4, 19, 12, 0), cost=190.0, amenities=[]),
    4: Reservation(property_id=8, status="Pending", client_name="Bob Johnson", client_phone="8888888888",
                       arrival=datetime(2024, 5, 17, 12, 0), departure=datetime(2024, 5, 20, 12, 0), cost=230.0, amenities=["crib", "extra bed"]),
    5: Reservation(property_id=7, status="OnGoing", client_name="Emily Wilson", client_phone="9999999999",
                       arrival=datetime(2024, 6, 8, 12, 0), departure=datetime(2024, 6, 11, 12, 0), cost=210.0, amenities=[]),
    6: Reservation(property_id=6, status="Pending", client_name="Michael Martinez", client_phone="1111111111",
                       arrival=datetime(2024, 4, 19, 12, 0), departure=datetime(2024, 4, 22, 12, 0), cost=240.0, amenities=["extra bed"]),
    7: Reservation(property_id=3, status="OnGoing", client_name="Olivia Davis", client_phone="2222222222",
                       arrival=datetime(2024, 3, 20, 12, 0), departure=datetime(2024, 3, 23, 12, 0), cost=210.0, amenities=[]),
    8: Reservation(property_id=2, status="Pending", client_name="David Garcia", client_phone="3333333333",
                       arrival=datetime(2024, 3, 21, 12, 0), departure=datetime(2024, 3, 24, 12, 0), cost=260.0, amenities=[]),
    9: Reservation(property_id=1, status="OnGoing", client_name="Sophia Rodriguez", client_phone="4444444444",
                       arrival=datetime(2024, 3, 22, 12, 0), departure=datetime(2024, 3, 25, 12, 0), cost=220.0, amenities=["crib"]),
    10: Reservation(property_id=10, status="Pending", client_name="James Hernandez", client_phone="1155555555",
                        arrival=datetime(2024, 3, 23, 12, 0), departure=datetime(2024, 3, 26, 12, 0), cost=280.0, amenities=[])
}

lock = Lock()

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"]
)


@router.get("/", status_code=200)
def get_reservation_list() -> Dict[int, Reservation]:
    return reservation_data


@router.get("/{property_id}", status_code=200)
def get_reservations_by_property_id(property_id: int) -> List[Reservation]:
    reservations = []
    for reservation in reservation_data.values():
        if reservation.property_id == property_id:
            reservations.append(reservation)
    return reservations


@router.post("/", status_code=201)
def create_reservation(reservation: Reservation) -> ReservationInDB:
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
        amenities=saved_reservation.amenities,
        id=id
    )
    return reservation_in_db


@router.put("/{reservation_id}", status_code=200)
def update_reservation(reservation_id: int, reservation: Reservation) -> ReservationInDB:
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
        amenities=saved_reservation.amenities,
        id=reservation_id
    )
    return reservation_in_db


@router.delete("/{reservation_id}", status_code=200)
def delete_reservation(reservation_id: int) -> Dict[int, Reservation]:
    del reservation_data[reservation_id]
    return reservation_data