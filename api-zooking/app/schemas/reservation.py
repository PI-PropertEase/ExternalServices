from pydantic import BaseModel
from datetime import datetime

class ReservationBase(BaseModel):
    property_id: int
    status: str
    client_name: str
    client_phone: str
    arrival: datetime
    departure: datetime
    cost: float

class ReservationInDb(ReservationBase):
    id: int