from typing import List, Optional
from base_schemas.reservation import ReservationBase

class Reservation(ReservationBase):
    amenities: List[str]

class ReservationInDB(Reservation):
    id: int