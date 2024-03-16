from pydantic import BaseModel, validator
from datetime import datetime

class ReservationBase(BaseModel):
    property_id: int
    status: str
    client_name: str
    client_phone: str
    arrival: datetime
    departure: datetime
    cost: float

    @validator('departure')
    def departure_later_then_arrival(cls, v, values):
        if v <= values['arrival']:
            raise ValueError('Departure date must be after arrival date')
        return v

class ReservationInDb(ReservationBase):
    id: int