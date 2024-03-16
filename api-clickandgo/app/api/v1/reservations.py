from fastapi import APIRouter
from typing import Dict, List
from app.schemas.reservation import ReservationBase, ReservationInDb
from datetime import datetime

reservation_data = {
    1: ReservationBase(property_id=10, status="OnGoing", client_name="John Smith", client_phone="5555555555",
                       arrival=datetime(2024, 3, 14, 12, 0), departure=datetime(2024, 3, 16, 12, 0), cost=200.0),
    2: ReservationBase(property_id=9, status="Pending", client_name="Jane Doe", client_phone="6666666666",
                       arrival=datetime(2024, 4, 15, 12, 0), departure=datetime(2024, 4, 18, 12, 0), cost=220.0),
    3: ReservationBase(property_id=8, status="OnGoing", client_name="Alice Brown", client_phone="7777777777",
                       arrival=datetime(2024, 4, 16, 12, 0), departure=datetime(2024, 4, 19, 12, 0), cost=190.0),
    4: ReservationBase(property_id=8, status="Pending", client_name="Bob Johnson", client_phone="8888888888",
                       arrival=datetime(2024, 5, 17, 12, 0), departure=datetime(2024, 5, 20, 12, 0), cost=230.0),
    5: ReservationBase(property_id=7, status="OnGoing", client_name="Emily Wilson", client_phone="9999999999",
                       arrival=datetime(2024, 6, 8, 12, 0), departure=datetime(2024, 6, 11, 12, 0), cost=210.0),
    6: ReservationBase(property_id=6, status="Pending", client_name="Michael Martinez", client_phone="1111111111",
                       arrival=datetime(2024, 4, 19, 12, 0), departure=datetime(2024, 4, 22, 12, 0), cost=240.0),
    7: ReservationBase(property_id=3, status="OnGoing", client_name="Olivia Davis", client_phone="2222222222",
                       arrival=datetime(2024, 3, 20, 12, 0), departure=datetime(2024, 3, 23, 12, 0), cost=210.0),
    8: ReservationBase(property_id=2, status="Pending", client_name="David Garcia", client_phone="3333333333",
                       arrival=datetime(2024, 3, 21, 12, 0), departure=datetime(2024, 3, 24, 12, 0), cost=260.0),
    9: ReservationBase(property_id=1, status="OnGoing", client_name="Sophia Rodriguez", client_phone="4444444444",
                       arrival=datetime(2024, 3, 22, 12, 0), departure=datetime(2024, 3, 25, 12, 0), cost=220.0),
    10: ReservationBase(property_id=10, status="Pending", client_name="James Hernandez", client_phone="1155555555",
                        arrival=datetime(2024, 3, 23, 12, 0), departure=datetime(2024, 3, 26, 12, 0), cost=280.0)
}


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
def create_reservation(reservation: ReservationBase) -> ReservationInDb:
    id = len(reservation_data)+1
    reservation_data[id] = reservation
    saved_reservation = reservation_data[id]
    reservation_in_db = ReservationInDb(
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
def update_reservation(reservation_id: int, reservation: ReservationBase) -> ReservationInDb:
    reservation_data[reservation_id] = reservation
    saved_reservation = reservation_data[reservation_id]
    reservation_in_db = ReservationInDb(
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