from enum import Enum
from typing import Optional

from pydantic import BaseModel, validator, Field, EmailStr
from datetime import datetime


class ReservationStatus(str, Enum):
    CONFIRMED = "confirmed"
    PENDING = "pending"
    CANCELED = "canceled"


class ReservationBase(BaseModel):
    property_id: int
    client_email: str
    client_name: str
    client_phone: str
    arrival: datetime
    departure: datetime
    cost: float
    reservation_status: ReservationStatus

    @validator('departure')
    def departure_later_then_arrival(cls, v, values):
        if v <= values['arrival']:
            raise ValueError('Departure date must be after arrival date')
        return v


class ReservationBaseUpdate(BaseModel):
    reservation_status: Optional[ReservationStatus] = None



class ReservationInDB(ReservationBase):
    id: int
